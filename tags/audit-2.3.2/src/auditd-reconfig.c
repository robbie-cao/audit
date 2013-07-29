/* auditd-reconfig.c -- 
 * Copyright 2005 Red Hat Inc., Durham, North Carolina.
 * All Rights Reserved.
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 *
 * Authors:
 *   Steve Grubb <sgrubb@redhat.com>
 * 
 */

#include "config.h"
#include <pthread.h>
#include <signal.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <stdio.h>
#include "libaudit.h"
#include "auditd-event.h"
#include "auditd-config.h"
#include "private.h"

/* This is the configuration manager code */
static pthread_t config_thread;
static pthread_mutex_t config_lock;
static void *config_thread_main(void *arg);

void init_config_manager(void)
{
	pthread_mutex_init(&config_lock, NULL);
	audit_msg(LOG_DEBUG, "config_manager init complete");
}

int start_config_manager(struct auditd_reply_list *rep)
{
	int retval, rc = 0;
	
	retval = pthread_mutex_trylock(&config_lock);
	if (retval == 0) {
		pthread_attr_t detached;

		pthread_attr_init(&detached);
		pthread_attr_setdetachstate(&detached,
			PTHREAD_CREATE_DETACHED);

	        if (pthread_create(&config_thread, &detached,
        	                config_thread_main, rep) < 0) {
                	audit_msg(LOG_ERR,
			"Couldn't create config thread, no config changes");
			free(rep);
			pthread_mutex_unlock(&config_lock);
        	        rc = 1;
	        }
		pthread_attr_destroy(&detached);
	} else {
               	audit_msg(LOG_ERR, 
			"Config thread already running, no config changes");
		free(rep);
       	        rc = 1;
	}
	return rc;
}

void shutdown_config(void)
{
        pthread_cancel(config_thread);
}

static void *config_thread_main(void *arg)
{
	sigset_t sigs;
	struct auditd_reply_list *rep = (struct auditd_reply_list *)arg;
	struct daemon_conf new_config;
	extern int send_audit_event(int type, const char *str);

	/* This is a worker thread. Don't handle signals. */
	sigemptyset(&sigs);
	sigaddset(&sigs, SIGALRM);
	sigaddset(&sigs, SIGTERM);
	sigaddset(&sigs, SIGHUP);
	sigaddset(&sigs, SIGUSR1);
	sigaddset(&sigs, SIGUSR2);
	pthread_sigmask(SIG_SETMASK, &sigs, NULL);

	if (load_config(&new_config, TEST_AUDITD) == 0) {
		/* We will re-use the current reply */
		new_config.sender_uid = rep->reply.signal_info->uid;
		new_config.sender_pid = rep->reply.signal_info->pid;
		if (rep->reply.len > 24)
			new_config.sender_ctx = 
				strdup(rep->reply.signal_info->ctx);
		else
			new_config.sender_ctx = strdup("?"); 
		memcpy(rep->reply.msg.data, &new_config, sizeof(new_config));
		rep->reply.conf = (struct daemon_conf *)rep->reply.msg.data;
		rep->reply.type = AUDIT_DAEMON_RECONFIG;
		enqueue_event(rep);
	} else {
		// need to send a failed event message
		char txt[MAX_AUDIT_MESSAGE_LENGTH];
		snprintf(txt, sizeof(txt),
	    "reconfig aborted, sending auid=%u pid=%d subj=%s res=failed",
			rep->reply.signal_info->uid,
			rep->reply.signal_info->pid,
			(rep->reply.len > 24) ? 
				rep->reply.signal_info->ctx : "?");
		send_audit_event(AUDIT_DAEMON_CONFIG, txt);
		free_config(&new_config);
		free(rep);
	}

	pthread_mutex_unlock(&config_lock);
	return NULL;		
}

