Summary:        Portable Hardware Locality
Name:           hwloc
Version:        2.1.0
Release:        1%{?dist}
Vendor:         VMware, Inc.
Distribution:   Photon
License:        BSD
Url:            http://www.open-mpi.org/projects/hwloc
Group:          Applications/Utilities
Source0:        https://github.com/open-mpi/hwloc/archive/%{name}-%{version}.tar.gz
%define sha512  hwloc=3ad088db64135f86728c0bd93557a843977d4e1a2a8eee9a071bc2da9b7f3dae16dc213790067f8dc249fc1505735db5c009698b8e45ebc8693e9a7449ac7245

%description
The Portable Hardware Locality (hwloc) software package provides a portable abstraction (across OS, versions, architectures, ...)
of the hierarchical topology of modern architectures, including NUMA memory nodes, sockets, shared caches, cores and simultaneous multithreading.
It also gathers various system attributes such as cache and memory information as well as the locality of I/O devices such as network interfaces, InfiniBand HCAs or GPUs.

%package        devel
Summary:        Development libraries for hwloc
Requires:       %{name} = %{version}-%{release}

%description    devel
Development libraries for hwloc

%package        docs
Summary:        Documentation for hwloc
Requires:       %{name} = %{version}-%{release}

%description    docs
Documentation for hwloc

%prep
%autosetup -n hwloc-hwloc-%{version}

%build
sh autogen.sh
%configure
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} %{?_smp_mflags} install
find %{buildroot} -name '*.la' -delete

# Pre-install
%pre

    # First argument is 1 => New Installation
    # First argument is 2 => Upgrade

# Post-install
%post

    # First argument is 1 => New Installation
    # First argument is 2 => Upgrade

    /sbin/ldconfig

# Pre-uninstall
%preun

    # First argument is 0 => Uninstall
    # First argument is 1 => Upgrade

# Post-uninstall
%postun

    /sbin/ldconfig

    # First argument is 0 => Uninstall
    # First argument is 1 => Upgrade

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/*
%ifarch x86_64
%{_sbindir}/*
%endif
%{_libdir}/*.so.*
%{_sysconfdir}/bash_completion.d/hwloc-completion.bash

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%files docs
%defattr(-,root,root)
%{_mandir}/*
%{_docdir}/*
%{_datadir}/%{name}/*

%changelog
* Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 2.1.0-1
- Automatic Version Bump
* Thu Apr 29 2021 Gerrit Photon <photon-checkins@vmware.com> 2.4.1-1
- Automatic Version Bump
* Tue Sep 29 2020 Gerrit Photon <photon-checkins@vmware.com> 2.3.0-1
- Automatic Version Bump
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 2.2.0-1
- Automatic Version Bump
* Tue Jul 14 2020 Michelle Wang <michellew@vmware.com> 2.1.0-2
- exclude %{_sbindir}/* hwloc aarch64 rpm
* Mon Nov 25 2019 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.1.0-1
- Initial build.  First version.
