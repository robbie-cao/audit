/* typetab.h --
 * Copyright 2007-09,2011-12,2014-16 Red Hat Inc., Durham, North Carolina.
 * All Rights Reserved.
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation; either
 * version 2.1 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this library; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 *
 * Authors:
 *      Steve Grubb <sgrubb@redhat.com>
 */


_S(AUPARSE_TYPE_UID,		"auid"		)
_S(AUPARSE_TYPE_UID,		"uid"		)
_S(AUPARSE_TYPE_UID,		"euid"		)
_S(AUPARSE_TYPE_UID,		"suid"		)
_S(AUPARSE_TYPE_UID,		"fsuid"		)
_S(AUPARSE_TYPE_UID,		"ouid"		)
_S(AUPARSE_TYPE_UID,		"oauid"		)
_S(AUPARSE_TYPE_UID,		"iuid"		)
_S(AUPARSE_TYPE_UID,		"id"		)
_S(AUPARSE_TYPE_UID,		"inode_uid"	)
_S(AUPARSE_TYPE_UID,		"sauid"		)
_S(AUPARSE_TYPE_UID,		"obj_uid"	)
_S(AUPARSE_TYPE_GID,		"obj_gid"	)
_S(AUPARSE_TYPE_GID,		"gid"		)
_S(AUPARSE_TYPE_GID,		"egid"		)
_S(AUPARSE_TYPE_GID,		"sgid"		)
_S(AUPARSE_TYPE_GID,		"fsgid"		)
_S(AUPARSE_TYPE_GID,		"ogid"		)
_S(AUPARSE_TYPE_GID,		"igid"		)
_S(AUPARSE_TYPE_GID,		"inode_gid"	)
_S(AUPARSE_TYPE_GID,		"new_gid"	)
_S(AUPARSE_TYPE_SYSCALL,	"syscall"	)
_S(AUPARSE_TYPE_ARCH,		"arch"		)
_S(AUPARSE_TYPE_EXIT,		"exit"		)
_S(AUPARSE_TYPE_ESCAPED,	"path"		)
_S(AUPARSE_TYPE_ESCAPED,	"comm"		)
_S(AUPARSE_TYPE_ESCAPED,	"exe"		)
_S(AUPARSE_TYPE_ESCAPED,	"file"		)
_S(AUPARSE_TYPE_ESCAPED,	"name"		)
_S(AUPARSE_TYPE_ESCAPED,	"watch"		)
_S(AUPARSE_TYPE_ESCAPED,	"cwd"		)
_S(AUPARSE_TYPE_ESCAPED,	"cmd"		)
_S(AUPARSE_TYPE_ESCAPED,	"acct"		)
_S(AUPARSE_TYPE_ESCAPED,	"dir"		)
_S(AUPARSE_TYPE_ESCAPED,	"key"		)
_S(AUPARSE_TYPE_ESCAPED,	"vm"		)
_S(AUPARSE_TYPE_ESCAPED,	"old-chardev"	)
_S(AUPARSE_TYPE_ESCAPED,	"new-chardev"	)
_S(AUPARSE_TYPE_ESCAPED,	"old-disk"	)
_S(AUPARSE_TYPE_ESCAPED,	"new-disk"	)
_S(AUPARSE_TYPE_ESCAPED,	"old-fs"	)
_S(AUPARSE_TYPE_ESCAPED,	"new-fs"	)
_S(AUPARSE_TYPE_ESCAPED,	"old-net"	)
_S(AUPARSE_TYPE_ESCAPED,	"new-net"	)
_S(AUPARSE_TYPE_ESCAPED,	"device"	)
_S(AUPARSE_TYPE_ESCAPED,	"cgroup"	)
_S(AUPARSE_TYPE_PERM,		"perm"		)
_S(AUPARSE_TYPE_PERM,		"perm_mask"	)
_S(AUPARSE_TYPE_MODE,		"mode"		)
_S(AUPARSE_TYPE_SOCKADDR,	"saddr"		)
//_S(AUPARSE_TYPE_FLAGS,		"flags"		)
_S(AUPARSE_TYPE_PROMISC,	"prom"		)
_S(AUPARSE_TYPE_PROMISC,	"old_prom"	)
_S(AUPARSE_TYPE_CAPABILITY,	"capability"	)
_S(AUPARSE_TYPE_SUCCESS,	"res"		)
_S(AUPARSE_TYPE_SUCCESS,	"result"	)
_S(AUPARSE_TYPE_A0,		"a0"		)
_S(AUPARSE_TYPE_A1,		"a1"		)
_S(AUPARSE_TYPE_A2,		"a2"		)
_S(AUPARSE_TYPE_A3,		"a3"		)
_S(AUPARSE_TYPE_SIGNAL,		"sig"		)
_S(AUPARSE_TYPE_LIST,		"list"		)
_S(AUPARSE_TYPE_TTY_DATA,	"data"		)
_S(AUPARSE_TYPE_SESSION,	"ses"		)
_S(AUPARSE_TYPE_CAP_BITMAP,	"cap_pi"	)
_S(AUPARSE_TYPE_CAP_BITMAP,	"cap_pe"	)
_S(AUPARSE_TYPE_CAP_BITMAP,	"cap_pp"	)
_S(AUPARSE_TYPE_CAP_BITMAP,	"cap_fi"	)
_S(AUPARSE_TYPE_CAP_BITMAP,	"cap_fp"	)
_S(AUPARSE_TYPE_CAP_BITMAP,	"fp"		)
_S(AUPARSE_TYPE_CAP_BITMAP,	"fi"		)
_S(AUPARSE_TYPE_CAP_BITMAP,	"fe"		)
_S(AUPARSE_TYPE_CAP_BITMAP,	"old_pp"	)
_S(AUPARSE_TYPE_CAP_BITMAP,	"old_pi"	)
_S(AUPARSE_TYPE_CAP_BITMAP,	"old_pe"	)
_S(AUPARSE_TYPE_CAP_BITMAP,	"new_pp"	)
_S(AUPARSE_TYPE_CAP_BITMAP,	"new_pi"	)
_S(AUPARSE_TYPE_CAP_BITMAP,	"new_pe"	)
_S(AUPARSE_TYPE_NFPROTO,	"family"	)
_S(AUPARSE_TYPE_ICMPTYPE,	"icmptype"	)
_S(AUPARSE_TYPE_PROTOCOL,	"proto"		)
_S(AUPARSE_TYPE_ADDR,		"addr"		)
#ifdef WITH_APPARMOR
_S(AUPARSE_TYPE_ESCAPED,	"apparmor"	)
_S(AUPARSE_TYPE_ESCAPED,	"operation"	)
_S(AUPARSE_TYPE_ESCAPED,	"denied_mask"	)
_S(AUPARSE_TYPE_ESCAPED,	"info"		)
_S(AUPARSE_TYPE_ESCAPED,	"profile"	)
_S(AUPARSE_TYPE_ESCAPED,	"requested_mask")
#endif
_S(AUPARSE_TYPE_PERSONALITY,	"per"		)
_S(AUPARSE_TYPE_SECCOMP,	"code"		)
_S(AUPARSE_TYPE_ESCAPED,	"old-rng"	)
_S(AUPARSE_TYPE_ESCAPED,	"new-rng"	)
_S(AUPARSE_TYPE_OFLAG,		"oflag"		)
_S(AUPARSE_TYPE_ESCAPED,	"ocomm"		)
_S(AUPARSE_TYPE_MMAP,		"flags"		)
_S(AUPARSE_TYPE_SIGNAL,		"sigev_signo"	)
_S(AUPARSE_TYPE_MAC_LABEL,	"subj"		)
_S(AUPARSE_TYPE_MAC_LABEL,	"obj"		)
_S(AUPARSE_TYPE_MAC_LABEL,	"scontext"	)
_S(AUPARSE_TYPE_MAC_LABEL,	"tcontext"	)
_S(AUPARSE_TYPE_MAC_LABEL,	"vm-ctx"	)
_S(AUPARSE_TYPE_MAC_LABEL,	"img-ctx"	)
_S(AUPARSE_TYPE_PROCTITLE,	"proctitle"	)
_S(AUPARSE_TYPE_ESCAPED,	"grp"		)
_S(AUPARSE_TYPE_ESCAPED,	"new_group"	)
_S(AUPARSE_TYPE_HOOK,		"hook"		)

