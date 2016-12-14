/*
* classify-llist.h - Header file for classify-llist.c
* Copyright (c) 2016 Red Hat Inc., Durham, North Carolina.
* All Rights Reserved.
*
* This software may be freely redistributed and/or modified under the
* terms of the GNU General Public License as published by the Free
* Software Foundation; either version 2, or (at your option) any
* later version.
*
* This program is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
* GNU General Public License for more details.
*
* You should have received a copy of the GNU General Public License
* along with this program; see the file COPYING. If not, write to the
* Free Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
*
* Authors:
*   Steve Grubb <sgrubb@redhat.com>
*/

#ifndef CLASSIFY_LLIST_HEADER
#define CLASSIFY_LLIST_HEADER

#include "config.h"
#include <stdint.h>
#include "private.h"

/* This is the node of the linked list. Number & item are the only elements
 * at this time. Any data elements that are per item goes here. */
typedef struct _data_node {
  uint32_t num;		// The number
  void *data;		// Extra spot for data
  struct _data_node *next;	// Next string node pointer
} data_node;

/* This is the linked list head. Only data elements that are 1 per
 * event goes here. */
typedef struct {
  data_node *head;		// List head
  data_node *cur;		// Pointer to current node
  void (*cleanup)(void *); // Function to call when releasing memory
  unsigned int cnt;	// How many items in this list
} cllist;

static inline void cllist_first(cllist *l) { l->cur = l->head; }
static inline data_node *cllist_get_cur(cllist *l) { return l->cur; }

AUDIT_HIDDEN_START

void cllist_create(cllist *l, void (*cleanup)(void *));
void cllist_clear(cllist* l);
data_node *cllist_next(cllist *l);
void cllist_append(cllist *l, uint32_t num, void *data);

AUDIT_HIDDEN_END

#endif

