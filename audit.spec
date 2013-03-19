%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

# Do we want systemd?
%if 0%{?!nosystemd:1}
%define WITH_SYSTEMD 1
%else
%define WITH_SYSTEMD 0
%endif

Summary: User space tools for 2.6 kernel auditing
Name: audit
Version: 2.2.3
Release: 1
License: GPLv2+
Group: System Environment/Daemons
URL: http://people.redhat.com/sgrubb/audit/
Source0: http://people.redhat.com/sgrubb/audit/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: swig python-devel
BuildRequires: tcp_wrappers-devel krb5-devel libcap-ng-devel
BuildRequires: kernel-headers >= 2.6.29
Requires: %{name}-libs = %{version}-%{release}
%if %{WITH_SYSTEMD}
BuildRequires: systemd-units
Requires(post): systemd-units systemd-sysv chkconfig coreutils
Requires(preun): systemd-units
Requires(postun): systemd-units coreutils
%else
Requires: chkconfig
%endif

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
Summary: Header files for libaudit
License: LGPLv2+
Group: Development/Libraries
Requires: %{name}-libs = %{version}-%{release}
Requires: kernel-headers >= 2.6.29

%description libs-devel
The audit-libs-devel package contains the header files needed for
developing applications that need to use the audit framework libraries.

%package libs-static
Summary: Static version of libaudit library
License: LGPLv2+
Group: Development/Libraries
Requires: kernel-headers >= 2.6.29

%description libs-static
The audit-libs-static package contains the static libraries
needed for developing applications that need to use static audit
framework libraries

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
BuildRequires: libprelude-devel >= 0.9.16
Requires: %{name} = %{version}-%{release}
Requires: %{name}-libs = %{version}-%{release}
Requires: openldap

%description -n audispd-plugins
The audispd-plugins package provides plugins for the real-time
interface to the audit system, audispd. These plugins can do things
like relay events to remote machines or analyze events for suspicious
behavior.

%prep
%setup -q

%build
%configure --sbindir=/sbin --libdir=/%{_lib} --with-python=yes --with-prelude --with-libwrap --enable-gssapi-krb5=yes --with-libcap-ng=yes \
%if %{WITH_SYSTEMD}
	--enable-systemd
%endif

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/{sbin,etc/audispd/plugins.d}
%if !%{WITH_SYSTEMD}
mkdir -p $RPM_BUILD_ROOT/{etc/{sysconfig,rc.d/init.d}}
%endif
mkdir -p $RPM_BUILD_ROOT/%{_mandir}/{man5,man8}
mkdir -p $RPM_BUILD_ROOT/%{_lib}
mkdir -p $RPM_BUILD_ROOT/%{_libdir}/audit
mkdir -p $RPM_BUILD_ROOT/%{_var}/log/audit
mkdir -p $RPM_BUILD_ROOT/%{_var}/spool/audit
make DESTDIR=$RPM_BUILD_ROOT install

mkdir -p $RPM_BUILD_ROOT/%{_libdir}
# This winds up in the wrong place when libtool is involved
mv $RPM_BUILD_ROOT/%{_lib}/libaudit.a $RPM_BUILD_ROOT%{_libdir}
mv $RPM_BUILD_ROOT/%{_lib}/libauparse.a $RPM_BUILD_ROOT%{_libdir}
curdir=`pwd`
cd $RPM_BUILD_ROOT/%{_libdir}
LIBNAME=`basename \`ls $RPM_BUILD_ROOT/%{_lib}/libaudit.so.1.*.*\``
ln -s ../../%{_lib}/$LIBNAME libaudit.so
LIBNAME=`basename \`ls $RPM_BUILD_ROOT/%{_lib}/libauparse.so.0.*.*\``
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
touch -r ./audit.spec $RPM_BUILD_ROOT/usr/share/man/man5/libaudit.conf.5.gz

%check
make check

%clean
rm -rf $RPM_BUILD_ROOT

%post libs -p /sbin/ldconfig

%post
%if %{WITH_SYSTEMD}
%systemd_post auditd.service
%else
/sbin/chkconfig --add auditd
%endif

%preun
%if %{WITH_SYSTEMD}
%systemd_preun auditd.service
%else
if [ $1 -eq 0 ]; then
   /sbin/service auditd stop > /dev/null 2>&1
   /sbin/chkconfig --del auditd
fi
%endif

%postun libs -p /sbin/ldconfig

%postun
%if %{WITH_SYSTEMD}
%systemd_postun_with_restart auditd.service
%else
if [ $1 -ge 1 ]; then
   /sbin/service auditd condrestart > /dev/null 2>&1 || :
fi
%endif

%files libs
%defattr(-,root,root,-)
%attr(755,root,root) /%{_lib}/libaudit.so.1*
%attr(755,root,root) /%{_lib}/libauparse.*
%config(noreplace) %attr(640,root,root) /etc/libaudit.conf
%{_mandir}/man5/libaudit.conf.5.gz

%files libs-devel
%defattr(-,root,root,-)
%doc contrib/skeleton.c contrib/plugin
%{_libdir}/libaudit.so
%{_libdir}/libauparse.so
%{_includedir}/libaudit.h
%{_includedir}/auparse.h
%{_includedir}/auparse-defs.h
%{_mandir}/man3/*

%files libs-static
%defattr(-,root,root,-)
%{_libdir}/libaudit.a
%{_libdir}/libauparse.a

%files libs-python
%defattr(-,root,root,-)
%attr(755,root,root) %{python_sitearch}/_audit.so
%attr(755,root,root) %{python_sitearch}/auparse.so
%{python_sitearch}/audit.py*

%files
%defattr(-,root,root,-)
%doc  README COPYING ChangeLog contrib/capp.rules contrib/nispom.rules contrib/lspp.rules contrib/stig.rules init.d/auditd.cron
%attr(644,root,root) %{_mandir}/man8/audispd.8.gz
%attr(644,root,root) %{_mandir}/man8/auditctl.8.gz
%attr(644,root,root) %{_mandir}/man8/auditd.8.gz
%attr(644,root,root) %{_mandir}/man8/aureport.8.gz
%attr(644,root,root) %{_mandir}/man8/ausearch.8.gz
%attr(644,root,root) %{_mandir}/man8/autrace.8.gz
%attr(644,root,root) %{_mandir}/man8/aulast.8.gz
%attr(644,root,root) %{_mandir}/man8/aulastlog.8.gz
%attr(644,root,root) %{_mandir}/man8/auvirt.8.gz
%attr(644,root,root) %{_mandir}/man8/ausyscall.8.gz
%attr(644,root,root) %{_mandir}/man7/audit.rules.7.gz
%attr(644,root,root) %{_mandir}/man5/auditd.conf.5.gz
%attr(644,root,root) %{_mandir}/man5/audispd.conf.5.gz
%attr(644,root,root) %{_mandir}/man5/ausearch-expression.5.gz
%attr(750,root,root) /sbin/auditctl
%attr(750,root,root) /sbin/auditd
%attr(755,root,root) /sbin/ausearch
%attr(755,root,root) /sbin/aureport
%attr(750,root,root) /sbin/autrace
%attr(750,root,root) /sbin/audispd
%attr(755,root,root) %{_bindir}/aulast
%attr(755,root,root) %{_bindir}/aulastlog
%attr(755,root,root) %{_bindir}/ausyscall
%attr(755,root,root) %{_bindir}/auvirt
%if %{WITH_SYSTEMD}
%attr(640,root,root) %{_unitdir}/auditd.service
%else
%attr(755,root,root) /etc/rc.d/init.d/auditd
%config(noreplace) %attr(640,root,root) /etc/sysconfig/auditd
%endif
%attr(750,root,root) %dir %{_var}/log/audit
%attr(750,root,root) %dir /etc/audit
%attr(750,root,root) %dir /etc/audisp
%attr(750,root,root) %dir /etc/audisp/plugins.d
%config(noreplace) %attr(640,root,root) /etc/audit/auditd.conf
%config(noreplace) %attr(640,root,root) /etc/audit/audit.rules
%config(noreplace) %attr(640,root,root) /etc/audisp/audispd.conf
%config(noreplace) %attr(640,root,root) /etc/audisp/plugins.d/af_unix.conf
%config(noreplace) %attr(640,root,root) /etc/audisp/plugins.d/syslog.conf

%files -n audispd-plugins
%defattr(-,root,root,-)
%attr(644,root,root) %{_mandir}/man8/audispd-zos-remote.8.gz
%attr(644,root,root) %{_mandir}/man5/zos-remote.conf.5.gz
%config(noreplace) %attr(640,root,root) /etc/audisp/plugins.d/audispd-zos-remote.conf
%config(noreplace) %attr(640,root,root) /etc/audisp/zos-remote.conf
%attr(750,root,root) /sbin/audispd-zos-remote
%config(noreplace) %attr(640,root,root) /etc/audisp/plugins.d/au-prelude.conf
%config(noreplace) %attr(640,root,root) /etc/audisp/audisp-prelude.conf
%attr(750,root,root) /sbin/audisp-prelude
%attr(644,root,root) %{_mandir}/man5/audisp-prelude.conf.5.gz
%attr(644,root,root) %{_mandir}/man8/audisp-prelude.8.gz
%config(noreplace) %attr(640,root,root) /etc/audisp/audisp-remote.conf
%config(noreplace) %attr(640,root,root) /etc/audisp/plugins.d/au-remote.conf
%attr(750,root,root) /sbin/audisp-remote
%attr(700,root,root) %dir %{_var}/spool/audit
%attr(644,root,root) %{_mandir}/man5/audisp-remote.conf.5.gz
%attr(644,root,root) %{_mandir}/man8/audisp-remote.8.gz


%changelog
* Tue Mar 19 2012 Steve Grubb <sgrubb@redhat.com> 2.2.3-1
- New upstream release

