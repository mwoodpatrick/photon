Summary:        xinetd -- A better inetd.
Name:           xinetd
Version:        2.3.15
Release:        10%{?dist}
License:        BSD
Group:          System Environment/Daemons
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            http://www.xinetd.org
Source0:        https://github.com/xinetd-org/xinetd/archive/%{name}-%{version}.tar.gz
%define sha512 %{name}=9d6fee1fbc90329629d84086ae7de5cd51c25af7b68e52aa704d6f74bee5f0e3d54ca1bcf780f90f74ddc8d336ae0abb5e5e368d43c426a26b8dd2c4676d26aa
Source1:        xinetd.service

Patch0: CVE-2013-4342.patch

BuildRequires:  systemd-devel
BuildRequires:  libtirpc-devel

Requires:       systemd
Requires:       libtirpc

%description
Xinetd is a powerful inetd replacement. Xinetd has access control
mechanisms, extensive logging capabilities, the ability to make
services available based on time, can place limits on the number
of servers that can be started, and has a configurable defence
mechanism to protect against port scanners, among other things.

%prep
%autosetup -p1

%build
%configure
export LDFLAGS="${LDFLAGS} $(pkg-config --libs libtirpc)"
export CFLAGS="${CFLAGS} $(pkg-config --cflags libtirpc)"
%make_build

%install
mkdir -p %{buildroot}%{_sysconfdir}/%{name}.d \
         %{buildroot}%{_unitdir}

%make_install %{?_smp_mflags} \
    DAEMONDIR=%{buildroot}%{_sbindir} \
    MANDIR=%{buildroot}%{_mandir}
install -m 0600 contrib/%{name}.conf %{buildroot}%{_sysconfdir}/
cp contrib/%{name}.d/* %{buildroot}%{_sysconfdir}/%{name}.d
mkdir -p %{buildroot}%{_unitdir}
cp %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service

install -vdm755 %{buildroot}%{_libdir}/systemd/system-preset
echo "disable xinetd.service" > %{buildroot}%{_libdir}/systemd/system-preset/50-%{name}.preset

%clean
rm -rf %{buildroot}

%post
%systemd_post xinetd.service

%preun
%systemd_preun xinetd.service

%postun
%systemd_postun_with_restart xinetd.service

%files
%defattr(-, root, root)
%doc CHANGELOG COPYRIGHT README %{name}/sample.conf contrib/empty.conf
%{_sbindir}/*
%{_datadir}/man/*/*
%attr(0750, root, root) %config(noreplace) %{_sysconfdir}/%{name}.conf
%attr(0750, root, root) %config(noreplace) %{_sysconfdir}/%{name}.d/*
%{_unitdir}/%{name}.service
%{_libdir}/systemd/system-preset/50-%{name}.preset

%changelog
*   Thu Jun 29 2023 Roye Eshed <eshedr@vmware.com> 2.3.15-10
-   Fix for CVE-2013-4342
*   Tue Sep 25 2018 Alexey Makhalov <amakhalov@vmware.com> 2.3.15-9
-   Use libtirpc
*   Fri Oct 13 2017 Alexey Makhalov <amakhalov@vmware.com> 2.3.15-8
-   Use standard configure macros
*   Thu Jun 29 2017 Divya Thaluru <dthaluru@vmware.com>  2.3.15-7
-   Disabled xinetd service by default
*   Thu May 26 2016 Divya Thaluru <dthaluru@vmware.com>  2.3.15-6
-   Fixed logic to restart the active services after upgrade
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.3.15-5
-   GA - Bump release of all rpms
*   Wed May 4 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.3.15-4
-   Fix upgrade issues
*   Thu Dec 10 2015 Xiaolin Li <xiaolinl@vmware.com>  2.3.15-3
-   Add systemd to Requires and BuildRequires.
*   Thu Dec 03 2015 Xiaolin Li  <xiaolinl@vmware.com> 2.3.15-2
-   Remove rc files
*   Fri Aug 07 2015 Xiaolin Li  <xiaolinl@vmware.com> 2.3.15-1
-   Add xinetd library to photon
*   Sun Sep 07 2003 Steve Grubb <linux_4ever@yahoo.com>
-   Refined installation and added services.
