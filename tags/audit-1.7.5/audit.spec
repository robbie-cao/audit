%define sca_version 0.4.8
%define sca_release 1
%define selinux_variants mls strict targeted
%define selinux_policyver 3.2.5 
%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Summary: User space tools for 2.6 kernel auditing
Name: audit
Version: 1.7.5
Release: 1
License: GPLv2+
Group: System Environment/Daemons
URL: http://people.redhat.com/sgrubb/audit/
Source0: http://people.redhat.com/sgrubb/audit/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: gettext-devel intltool libtool swig python-devel
BuildRequires: kernel-headers >= 2.6.18
BuildRequires: automake >= 1.9
BuildRequires: autoconf >= 2.59
Requires: %{name}-libs = %{version}-%{release}
Requires: chkconfig
Requires(pre): coreutils

%description
The audit package contains the user space utilities for
storing and searching the audit records generate by
the audit subsystem in the Linux 2.6 kernel.

%package libs
Summary: Dynamic library for libaudit
License: LGPLv2+
Group: Development/Libraries

%description libs
The audit-libs package contains the dynamic libraries needed for 
applications to use the audit framework.

%package libs-devel
Summary: Header files and static library for libaudit
License: LGPLv2+
Group: Development/Libraries
Requires: %{name}-libs = %{version}-%{release}
Requires: kernel-headers >= 2.6.18

%description libs-devel
The audit-libs-devel package contains the static libraries and header 
files needed for developing applications that need to use the audit 
framework libraries.

%package libs-python
Summary: Python bindings for libaudit
License: LGPLv2+
Group: Development/Libraries
Requires: %{name}-libs = %{version}-%{release}

%description libs-python
The audit-libs-python package contains the bindings so that libaudit
and libauparse can be used by python.

%package -n audispd-plugins
Summary: Plugins for the audit event dispatcher
License: GPLv2+
Group: System Environment/Daemons
BuildRequires: openldap-devel
%if "%{selinux_policyver}" != ""
BuildRequires: checkpolicy selinux-policy-devel >= %{selinux_policyver}
%endif
BuildRequires: libprelude-devel >= 0.9.16
Requires: %{name} = %{version}-%{release}
Requires: %{name}-libs = %{version}-%{release}
Requires: openldap
%if "%{selinux_policyver}" != ""
Requires: selinux-policy >= %{selinux_policyver}
%endif
Requires(post): /usr/sbin/semodule /sbin/restorecon
Requires(postun): /usr/sbin/semodule

%description -n audispd-plugins
The audispd-plugins package provides plugins for the real-time
interface to the audit system, audispd. These plugins can do things
like relay events to remote machines or analyze events for suspicious
behavior.

%package -n system-config-audit
Summary: Utility for editing audit configuration
Version: %{sca_version}
Release: %{sca_release}
License: GPLv2+
Group: Applications/System
BuildRequires: desktop-file-utils
Requires: pygtk2-libglade usermode usermode-gtk

%description -n system-config-audit
A graphical utility for editing audit configuration.

%prep
%setup -q
mkdir zos-remote-policy
cp -p audisp/plugins/zos-remote/policy/audispd-zos-remote.* zos-remote-policy

%build
(cd system-config-audit; ./autogen.sh)
%configure --sbindir=/sbin --libdir=/%{_lib} --with-prelude
make %{?_smp_mflags}
cd zos-remote-policy
for selinuxvariant in %{selinux_variants}
do
  if [ "${selinuxvariant}" = "mls" ]; then
    TYPE=mls-mls
  else
    TYPE=${selinuxvariant}-mcs
  fi
  make -f /usr/share/selinux/devel/Makefile
  mv audispd-zos-remote.pp audispd-zos-remote.pp.${selinuxvariant}
  make -f /usr/share/selinux/devel/Makefile clean
done
cd -

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/{sbin,etc/{sysconfig,audispd/plugins.d,rc.d/init.d}}
mkdir -p $RPM_BUILD_ROOT/%{_mandir}/{man5,man8}
mkdir -p $RPM_BUILD_ROOT/%{_lib}
mkdir -p $RPM_BUILD_ROOT/%{_libdir}/audit
mkdir -p $RPM_BUILD_ROOT/%{_var}/log/audit
make DESTDIR=$RPM_BUILD_ROOT %{?_smp_mflags} install
make -C system-config-audit DESTDIR=$RPM_BUILD_ROOT install-fedora
for selinuxvariant in %{selinux_variants}
do
  install -d $RPM_BUILD_ROOT/%{_datadir}/selinux/${selinuxvariant}
  install -p -m 644 zos-remote-policy/audispd-zos-remote.pp.${selinuxvariant} \
    $RPM_BUILD_ROOT/%{_datadir}/selinux/${selinuxvariant}/audispd-zos-remote.pp
done

mkdir -p $RPM_BUILD_ROOT/%{_libdir}
# This winds up in the wrong place when libtool is involved
mv $RPM_BUILD_ROOT/%{_lib}/libaudit.a $RPM_BUILD_ROOT%{_libdir}
mv $RPM_BUILD_ROOT/%{_lib}/libauparse.a $RPM_BUILD_ROOT%{_libdir}
curdir=`pwd`
cd $RPM_BUILD_ROOT/%{_libdir}
LIBNAME=`basename \`ls $RPM_BUILD_ROOT/%{_lib}/libaudit.so.*.*.*\``
ln -s ../../%{_lib}/$LIBNAME libaudit.so
LIBNAME=`basename \`ls $RPM_BUILD_ROOT/%{_lib}/libauparse.so.*.*.*\``
ln -s ../../%{_lib}/$LIBNAME libauparse.so
cd $curdir
# Remove these items so they don't get picked up.
rm -f $RPM_BUILD_ROOT/%{_lib}/libaudit.so
rm -f $RPM_BUILD_ROOT/%{_lib}/libauparse.so
rm -f $RPM_BUILD_ROOT/%{_lib}/libaudit.la
rm -f $RPM_BUILD_ROOT/%{_lib}/libauparse.la
rm -f $RPM_BUILD_ROOT/%{_libdir}/python?.?/site-packages/_audit.a
rm -f $RPM_BUILD_ROOT/%{_libdir}/python?.?/site-packages/_audit.la
rm -f $RPM_BUILD_ROOT/%{_libdir}/python?.?/site-packages/_auparse.a
rm -f $RPM_BUILD_ROOT/%{_libdir}/python?.?/site-packages/_auparse.la
rm -f $RPM_BUILD_ROOT/%{_libdir}/python?.?/site-packages/auparse.a
rm -f $RPM_BUILD_ROOT/%{_libdir}/python?.?/site-packages/auparse.la

# On platforms with 32 & 64 bit libs, we need to coordinate the timestamp
touch -r ./audit.spec $RPM_BUILD_ROOT/etc/libaudit.conf

%find_lang system-config-audit

desktop-file-install					\
	--dir $RPM_BUILD_ROOT/%{_datadir}/applications	\
	--delete-original				\
	system-config-audit/system-config-audit.desktop

# This is a reminder to enable it when tests
# aren't based on postfix uids
#% check
#make check

%clean
rm -rf $RPM_BUILD_ROOT
rm -rf zos-remote-policy

%post libs -p /sbin/ldconfig

%post -n audispd-plugins
for selinuxvariant in %{selinux_variants}
do
  /usr/sbin/semodule -s $selinuxvariant \
    -i %{_datadir}/selinux/$selinuxvariant/audispd-zos-remote.pp \
    &> /dev/null || :
done
/sbin/restorecon -F /sbin/audispd-zos-remote /etc/audisp/zos-remote.conf

%post
/sbin/chkconfig --add auditd
# This is to migrate users from audit-1.0.x installations
if [ -f /etc/auditd.conf ]; then
   mv /etc/auditd.conf /etc/audit/auditd.conf
fi
if [ -f /etc/audit.rules ]; then
   mv /etc/audit.rules /etc/audit/audit.rules
fi
# This is to enable the dispatcher option which was commented out
if [ -f /etc/audit/auditd.conf ]; then
   grep '^dispatcher' /etc/audit/auditd.conf >/dev/null
   if [ $? -eq 1 ] ; then
      tmp=`mktemp /etc/audit/auditd-post.XXXXXX`
      if [ -n $tmp ]; then
         sed 's|^#dispatcher|dispatcher|g' /etc/audit/auditd.conf > $tmp && \
         cat $tmp > /etc/audit/auditd.conf
         rm -f $tmp
      fi
   fi
fi

%preun
if [ $1 -eq 0 ]; then
   /sbin/service auditd stop > /dev/null 2>&1
   /sbin/chkconfig --del auditd
fi

%postun libs -p /sbin/ldconfig

%postun -n audispd-plugins
if [ $1 -eq 0 ]; then
 for selinuxvariant in %{selinux_variants}
 do
   /usr/sbin/semodule -s $selinuxvariant -r audispd-zos-remote &>/dev/null || :
 done
fi

%postun
if [ $1 -ge 1 ]; then
   /sbin/service auditd condrestart > /dev/null 2>&1 || :
fi

%files libs
%defattr(-,root,root)
%attr(755,root,root) /%{_lib}/libaudit.*
%attr(755,root,root) /%{_lib}/libauparse.*
%config(noreplace) %attr(640,root,root) /etc/libaudit.conf

%files libs-devel
%defattr(-,root,root)
%doc contrib/skeleton.c contrib/plugin
%{_libdir}/libaudit.a
%{_libdir}/libauparse.a
%{_libdir}/libaudit.so
%{_libdir}/libauparse.so
%{_includedir}/libaudit.h
%{_includedir}/auparse.h
%{_includedir}/auparse-defs.h
%{_mandir}/man3/*
%{_mandir}/man5/ausearch-expression.5.gz

%files libs-python
%defattr(-,root,root)
%attr(755,root,root) %{_libdir}/python?.?/site-packages/_audit.so
%attr(755,root,root) %{_libdir}/python?.?/site-packages/auparse.so
#%{_libdir}/python?.?/site-packages/auparse-*.egg-info
%{python_sitelib}/audit.py*

%files
%defattr(-,root,root,-)
%doc  README COPYING ChangeLog contrib/capp.rules contrib/nispom.rules contrib/lspp.rules contrib/stig.rules init.d/auditd.cron
%attr(644,root,root) %{_mandir}/man8/audispd.8.gz
%attr(644,root,root) %{_mandir}/man8/auditctl.8.gz
%attr(644,root,root) %{_mandir}/man8/auditd.8.gz
%attr(644,root,root) %{_mandir}/man8/aureport.8.gz
%attr(644,root,root) %{_mandir}/man8/ausearch.8.gz
%attr(644,root,root) %{_mandir}/man8/autrace.8.gz
%attr(644,root,root) %{_mandir}/man8/aulastlog.8.gz
%attr(644,root,root) %{_mandir}/man8/ausyscall.8.gz
%attr(644,root,root) %{_mandir}/man5/auditd.conf.5.gz
%attr(644,root,root) %{_mandir}/man5/audispd.conf.5.gz
%attr(750,root,root) /sbin/auditctl
%attr(750,root,root) /sbin/auditd
%attr(755,root,root) /sbin/ausearch
%attr(755,root,root) /sbin/aureport
%attr(750,root,root) /sbin/autrace
%attr(750,root,root) /sbin/audispd
%attr(750,root,root) %{_bindir}/aulastlog
%attr(755,root,root) %{_bindir}/ausyscall
%attr(755,root,root) /etc/rc.d/init.d/auditd
%attr(750,root,root) %{_var}/log/audit
%attr(750,root,root) %dir /etc/audit
%attr(750,root,root) %dir /etc/audisp
%attr(750,root,root) %dir /etc/audisp/plugins.d
%attr(750,root,root) %dir %{_libdir}/audit
%config(noreplace) %attr(640,root,root) /etc/audit/auditd.conf
%config(noreplace) %attr(640,root,root) /etc/audit/audit.rules
%config(noreplace) %attr(640,root,root) /etc/sysconfig/auditd
%config(noreplace) %attr(640,root,root) /etc/audisp/audispd.conf
%config(noreplace) %attr(640,root,root) /etc/audisp/plugins.d/af_unix.conf

%files -n audispd-plugins
%defattr(-,root,root,-)
%attr(640,root,root) /etc/audisp/plugins.d/syslog.conf
%attr(644,root,root) %{_mandir}/man8/audispd-zos-remote.8.gz
%attr(644,root,root) %{_mandir}/man5/zos-remote.conf.5.gz
%config(noreplace) %attr(640,root,root) /etc/audisp/plugins.d/audispd-zos-remote.conf
%config(noreplace) %attr(640,root,root) /etc/audisp/zos-remote.conf
%attr(750,root,root) /sbin/audispd-zos-remote
%attr(644,root,root) %{_datadir}/selinux/*/audispd-zos-remote.pp
%config(noreplace) %attr(640,root,root) /etc/audisp/plugins.d/au-prelude.conf
%config(noreplace) %attr(640,root,root) /etc/audisp/audisp-prelude.conf
%attr(750,root,root) /sbin/audisp-prelude
%attr(644,root,root) %{_mandir}/man5/audisp-prelude.conf.5.gz
%attr(644,root,root) %{_mandir}/man8/audisp-prelude.8.gz
%config(noreplace) %attr(640,root,root) /etc/audisp/audisp-remote.conf
%config(noreplace) %attr(640,root,root) /etc/audisp/plugins.d/au-remote.conf
%attr(750,root,root) /sbin/audisp-remote
%attr(644,root,root) %{_mandir}/man5/audisp-remote.conf.5.gz
%attr(644,root,root) %{_mandir}/man8/audisp-remote.8.gz

%files -n system-config-audit -f system-config-audit.lang
%defattr(-,root,root,-)
%doc system-config-audit/AUTHORS
%doc system-config-audit/COPYING
%doc system-config-audit/ChangeLog
%doc system-config-audit/NEWS
%doc system-config-audit/README
%{_bindir}/system-config-audit
%{_datadir}/applications/system-config-audit.desktop
%{_datadir}/system-config-audit
%{_libexecdir}/system-config-audit-server-real
%{_libexecdir}/system-config-audit-server
%config(noreplace) %{_sysconfdir}/pam.d/system-config-audit-server
%config(noreplace) %{_sysconfdir}/security/console.apps/system-config-audit-server

%changelog
* Mon Aug 25 2008 Steve Grubb <sgrubb@redhat.com> 1.7.5-1
- Update system-config-audit to 0.4.8
- Whole lot of bug fixes - see ChangeLog for details
- Reimplement auditd main loop using libev
- Add TCP listener to auditd to receive remote events

* Mon May 19 2008 Steve Grubb <sgrubb@redhat.com> 1.7.4-1
- Fix interpreting of keys in syscall records
- Interpret audit rule config change list fields
- Don't error on name=(null) PATH records in ausearch/report
- Add key report to aureport
- Fix --end today to be now
- Added python bindings for auparse_goto_record_num
- Update system-config-audit to 0.4.7 (Miloslav Trmac)
- Add support for the filetype field option in auditctl
- In audispd boost priority after starting children

* Fri May 09 2008 Steve Grubb <sgrubb@redhat.com> 1.7.3-1
- Fix path processing in AVC records.
- auparse_find_field_next() wasn't resetting field ptr going to next record.
- auparse_find_field() wasn't checking current field before iterating
- cleanup some string handling in audisp-prelude plugin
- Update auditctl man page
- Fix output of keys in ausearch interpretted mode
- Fix ausearch/report --start now to not be reset to midnight
- Added auparse_goto_record_num function
- Prelude plugin now uses auparse_goto_record_num to avoid skipping a record
- audispd now has a priority boost config option
- Look for laddr in avcs reported via prelude
- Detect page 0 mmaps and alert via prelude

* Wed Apr 09 2008 Steve Grubb <sgrubb@redhat.com> 1.7.2-1
- gen_table.c now includes IPC defines to avoid kernel headers wild goose chase 
- ausyscall program added for cross referencing syscall name and number info
- Add login session ID search capability to ausearch

* Tue Apr 08 2008 Steve Grubb <sgrubb@redhat.com> 1.7.1-1
- Remove LSB headers info for init scripts
- Fix buffer overflow in audit_log_user_command, again (#438840)
- Fix memory leak in EOE code in auditd (#440075)
- In auditctl, don't use new operators in legacy rule format
- Made a couple corrections in alpha & x86_64 syscall tables (Miloslav Trmac)
- Add example STIG rules file
- Add string table lookup performance improvement patch (Miloslav Trmac)
- auparse_find_field_next performance improvement

* Sun Mar 30 2008 Steve Grubb <sgrubb@redhat.com> 1.7-1
- Improve input error handling in audispd
- Improve end of event detection in auparse library
- Improve handling of abstract namespaces
- Add test mode for prelude plugin
- Handle user space avcs in prelude plugin
- Audit event serial number now recorded in idmef alert
- Add --just-one option to ausearch
- Fix watched account login detection for some failed login attempts
- Couple fixups in audit logging functions (Miloslav Trmac)
- Add support in auditctl for virtual keys
- Added new type for user space MAC policy load events
- auparse_find_field_next was not iterating correctly, fixed it
- Add idmef alerts for access or execution of watched file
- Fix buffer overflow in audit_log_user_command
- Add basic remote logging plugin - only sends & no flow control
- Update ausearch with interpret fixes from auparse

* Sun Mar 09 2008 Steve Grubb <sgrubb@redhat.com> 1.6.9-1
- Apply hidden attribute cleanup patch (Miloslav Trmac)
- Apply auparse expression interface patch (Miloslav Trmac)
- Fix potential memleak in audit event dispatcher
- Change default audispd queue depth to 80
- Update system-config-audit to version 0.4.6 (Miloslav Trmac)
- audisp-prelude alerts now controlled by config file
- Updated syscall table for 2.6.25 kernel
- Apply patch correcting acct field being misencoded (Miloslav Trmac)
- Added watched account login detection for prelude plugin

* Thu Feb 14 2008 Steve Grubb <sgrubb@redhat.com> 1.6.8-1
- Update for gcc 4.3
- Cleanup descriptors in audispd before running plugin
- Fix 'recent' keyword for aureport/search
- Fix SE Linux policy for zos_remote plugin
- Add event type for group password authentication attempts
- Couple of updates to the translation tables
- Add detection of failed group authentication to audisp-prelude

* Thu Jan 31 2008 Steve Grubb <sgrubb@redhat.com> 1.6.7-1
- In ausearch/report, prefer -if to stdin
- In ausearch/report, add new command line option --input-logs (#428860)
- Updated audisp-prelude based on feedback from prelude-devel
- Added prelude alert for promiscuous socket being opened
- Added prelude alert for SE Linux policy enforcement changes
- Added prelude alerts for Forbidden Login Locations and Time
- Applied patch to auparse fixing error handling of searching by
  interpreted value (Miloslav Trmac)

* Sat Jan 19 2008 Steve Grubb <sgrubb@redhat.com> 1.6.6-1
- Add prelude IDS plugin for IDMEF alerts
- Add --user option to aulastlog command
- Use desktop-file-install for system-config-audit

* Mon Jan 07 2008 Steve Grubb <sgrubb@redhat.com> 1.6.5-1
- Add more errno strings for exit codes in auditctl
- Fix config parser to allow either 0640 or 0600 for audit logs (#427062)
- Check for audit log being writable by owner in auditd
- If auditd logging was suspended, it can be resumed with SIGUSR2 (#251639)
- Updated CAPP, LSPP, and NISPOM rules for new capabilities
- Added aulastlog utility

* Sat Dec 29 2007 Steve Grubb <sgrubb@redhat.com> 1.6.4-1
- fchmod of log file was on wrong variable (#426934)
- Allow use of errno strings for exit codes in audit rules

* Thu Dec 27 2007 Steve Grubb <sgrubb@redhat.com> 1.6.3-1
- Add kernel release string to DEAMON_START events
- Fix keep_logs when num_logs option disabled (#325561)
- Fix auparse to handle node fields for syscall records
- Update system-config-audit to version 0.4.5 (Miloslav Trmac)
- Add keyword week-ago to aureport & ausearch start/end times
- Fix audit log permissions on rotate. If group is root 0400, otherwise 0440
- Add RACF zos remote audispd plugin (Klaus Kiwi)
- Add event queue overflow action to audispd

* Tue Sep 25 2007 Steve Grubb <sgrubb@redhat.com> 1.6.2-1
- Add support for searching by posix regular expressions in auparse
- Route DEAMON events into rt interface
- If event pipe is full, try again after doing local logging
- Optionally add node/machine name to records in audit daemon
- Update ausearch/aureport to specify nodes to search on
- Fix segfault interpretting saddr fields in avcs

* Sun Sep 2 2007 Steve Grubb <sgrubb@redhat.com> 1.6.1-1
- updated system-config-audit to 0.4.3 (Miloslav Trmac)
- External plugin support in place
- Add missing newline to string output of event dispatcher.
- Fix reference counting in auparse python bindings (#263961)
- Moved default af_unix plugin socket to /var/run/audispd_events

* Mon Aug 27 2007 Steve Grubb <sgrubb@redhat.com> 1.6-1
- Adding perm field should not set syscall added flag in auditctl
- Fix segfault when aureport -if option is used
- Fix auditctl to better check keys on rule lines
- Add support for audit by TTY and other new event types
- Auditd config option for group permission of audit logs
- Swig messed up a variable in ppc's python bindings causing crashes. (#251327)
- New audit event dispatcher
- Update syscall tables for 2.6.23 kernel

* Wed Jul 25 2007 Steve Grubb <sgrubb@redhat.com> 1.5.6-1
- Fix potential buffer overflow in print clone flags of auparse
- Add new App Armor types (John Johansen)
- Adjust Menu Location for system-config-audit (Miloslav Trmac)
- Fix python traceback parsing watches without perm statement (Miloslav Trmac)
- Added databuf_strcat function to auparse (John Dennis)
- Update auditctl to handle legacy kernels when putting a watch on a dir
- Fix invalid free and memory leak on reload in auditd (Miloslav Trmac)
- Fix clone flags in auparse (John Ramsdell)
- Add interpretation for F_SETFL of fcntl (John Ramsdell)
- Fix acct interpretation in auparse
- Makefile cleanups (John Ramsdell)

* Tue Jul 10 2007 Steve Grubb <sgrubb@redhat.com> 1.5.5-1
- Add system-config-audit (Miloslav Trmac)
- Correct bug in audit_make_equivalent function (Al Viro)

* Tue Jun 26 2007 Steve Grubb <sgrubb@redhat.com> 1.5.4-1
- Add feed interface to auparse library (John Dennis)
- Apply patch to libauparse for unresolved symbols (#241178)
- Apply patch to add line numbers for file events in libauparse (John Dennis)
- Change seresults to seresult in libauparse (John Dennis)
- Add unit32_t definition to swig (#244210)
- Add support for directory auditing
- Update acct field to be escaped

* Tue May 01 2007 Steve Grubb <sgrubb@redhat.com> 1.5.3-1
- Change buffer size to prevent truncation of DAEMON events with large labels
- Fix memory leaks in auparse (John Dennis)
- Update syscall tables for 2.6.21 kernel
- Update capp & lspp rules
- New python bindings for libauparse (John Dennis)

* Thu Apr 04 2007 Steve Grubb <sgrubb@redhat.com> 1.5.2-1
- New event dispatcher (James Antill)
- Apply patches fixing man pages and Makefile.am (Philipp Hahn)
- Apply patch correcting python libs permissions (Philipp Hahn)
- Fix auditd segfault on reload
- Add support for segfault anomaly message type
- Fix bug in auparse library for file pointers and descriptors
- Extract subject information out of daemon events for ausearch

* Tue Mar 20 2007 Steve Grubb <sgrubb@redhat.com> 1.5.1-1
- Updated autrace to monitor *at syscalls
- Add support in libaudit for AUDIT_BIT_TEST(^) and AUDIT_MASK_TEST (&)
- Finish reworking auditd config parser
- In auparse, interpret open, fcntl, and clone flags
- In auparse, when interpreting execve record types, run args through unencode
- Add support for OBJ_PID message type
- Event dispatcher updates

* Fri Mar 2 2007 Steve Grubb <sgrubb@redhat.com> 1.5-1
- NEW audit dispatcher program & plugin framework
- Correct hidden variables in libauparse
- Added NISPOM sample rules
- Verify accessibility of files passed in auparse_init
- Fix bug in parser library interpreting socketcalls
- Add support for stdio FILE pointer in auparse_init
- Adjust init script to allow anyone to status auditd (#230626)

* Tue Feb 20 2007 Steve Grubb <sgrubb@redhat.com> 1.4.2-1
- Add man pages
- Reduce text relocations in parser library
- Add -n option to auditd for no fork
- Add exec option to space_left, admin_space_left, disk_full,
  and disk_error - eg EXEC /usr/local/script

* Fri Feb 16 2007 Steve Grubb <sgrubb@redhat.com> 1.4.1-1
- updated audit_rule_fieldpair_data to handle perm correctly (#226780)
- Finished search options for audit parsing library
- Fix ausearch -se to work correctly
- Fix auditd init script for /usr on netdev (#228528)
- Parse avc seperms better when there are more than one

* Sun Feb 04 2007 Steve Grubb <sgrubb@redhat.com> 1.4-1
- New report about authentication attempts
- Updates for python 2.5
- update autrace to have resource usage mode
- update auditctl to support immutable config
- added audit_log_user_command function to libaudit api
- interpret capabilities
- added audit event parsing library
- updates for 2.6.20 kernel

* Sun Dec 10 2006 Steve Grubb <sgrubb@redhat.com> 1.3.1-1
- Fix a couple parsing problems (#217952)
- Add tgkill to S390* syscall tables (#218484)
- Fix error messages in ausearch/aureport
- Fix timestamp for libaudit.conf (#218053)

* Tue Nov 28 2006 Steve Grubb <sgrubb@redhat.com> 1.3-1
- ausearch & aureport implement uid/gid caching
- In ausearch & aureport, extract addr when hostname is unknown
- In ausearch & aureport, test audit log presence O_RDONLY
- New ausearch/aureport time keywords: recent, this-week, this-month, this-year
- Added --add & --delete option to aureport
- Update res parsing in config change events
- Increase the size on audit daemon buffers
- Parse avc_path records in ausearch/aureport
- ausearch has new output mode, raw, for extracting events
- ausearch/aureport can now read stdin
- Rework AVC processing in ausearch/aureport
- Added long options to ausearch and aureport

* Tue Oct 24 2006 Steve Grubb <sgrubb@redhat.com> 1.2.9-1
- In auditd if num_logs is zero, don't rotate on SIGUSR1 (#208834)
- Fix some defines in libaudit.h
- Some auditd config strings were not initialized in aureport (#211443)
- Updated man pages
- Add Netlabel event types to libaudit
- Update aureports to current audit event types
- Update autrace a little
- Deprecated all the old audit_rule functions from public API
- Drop auparse library for the moment

* Fri Sep 29 2006 Steve Grubb <sgrubb@redhat.com> 1.2.8-1
- Make internal auditd buffers bigger for context info
- Correct address resolving of hostname in logging functions
- Do not allow multiple msgtypes in same audit rule in auditctl (#207666)
- Only =, != operators for arch & inode fields in auditctl (#206427)
- Add disp_qos & dispatcher to auditd reconfigure
- Send sighup to child when no change in dispatcher during auditd reconfigure
- Cleanup file descriptor handling in auditd
- Updated audit message type table
- Remove watches from aureport since FS_WATCH is deprecated
- Add audit_log_avc back temporarily (#208152)
