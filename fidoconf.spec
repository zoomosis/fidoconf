%global ver_major 1
%global ver_minor 9
%global ver_patch 0
%global reldate 20201016
%global reltype C
# may be one of: C (current), R (release), S (stable)

# release number for Release: header
%global relnum 3

# on default static library is made but using 'rpmbuild --without static'
# produces a dynamic library
%if %_vendor == "alt"
    %def_with static
    %global  __arch_install_post %nil
%else
    %bcond_without static
%endif

# if you use 'rpmbuild --with debug' then debug binary is produced
%if %_vendor == "alt"
    %def_without debug
%else
    %bcond_with debug
%endif

%global debug_package %nil

# for generic build; will override for some distributions
%global vendor_prefix %nil
%global vendor_suffix %nil
%global pkg_group Applications/Communications

# for CentOS, Fedora and RHEL
%if %_vendor == "redhat"
    %global vendor_suffix %dist
%endif

# for ALT Linux
%if %_vendor == "alt"
    %global vendor_prefix %_vendor
    %global pkg_group Networking/FTN
%endif

%global main_name fidoconf
%if %{with static}
Name: %main_name-static
%else
Name: %main_name
%endif
Version: %ver_major.%ver_minor.%reldate%reltype
Release: %{vendor_prefix}%relnum%{vendor_suffix}
%if %_vendor != "redhat"
Group: %pkg_group
%endif
%if %{with static}
Summary: Common configuration static library for the Husky Project applications
%else
Summary: Common configuration dynamic library for the Husky Project applications
%endif
URL: https://github.com/huskyproject/%main_name/archive/v%ver_major.%ver_minor.%reldate.tar.gz
License: GPL
Source: %main_name-%ver_major.%ver_minor.%reldate.tar.gz
%if %{with static}
BuildRequires: huskylib-static huskylib-static-devel
BuildRequires: smapi-static smapi-static-devel
%else
BuildRequires: huskylib huskylib-devel
BuildRequires: smapi smapi-devel
Requires: huskylib smapi
%endif

%description
%summary


%package devel
%if %_vendor != "redhat"
Group: %pkg_group
%endif
Summary: Development headers for %main_name
%if %{with static}
BuildArch: noarch
%else
Requires: %name = %version-%release
%endif
%description devel
%summary


%package utils
%if %_vendor != "redhat"
Group: %pkg_group
%endif
Summary: Optional utilities for %name
%if ! %{with static}
Requires: %name = %version-%release
%endif
Provides: %name-utils = %version-%release
%description utils
%summary


%if %{with static}
    %global parser tparser-static
%else
    %global parser tparser
%endif
%package -n %parser
%if %_vendor != "redhat"
Group: %pkg_group
%endif
Summary: A utility for parsing and checking Husky Project configuration files
%if ! %{with static}
Requires: %name = %version-%release
%endif
%description -n %parser
%summary


%prep
%setup -q -n %main_name-%ver_major.%ver_minor.%reldate


%build
%if %{with static}
    %if %{with debug}
        %make_build DEBUG:=1
    %else
        %make_build
    %endif
%else
    %if %{with debug}
        %make_build DYNLIBS:=1 DEBUG:=1
    %else
        %make_build DYNLIBS:=1
    %endif
%endif
echo Install-name1:%_rpmdir/%_arch/%name-%version-%release.%_arch.rpm > /dev/null
%if %{with static}
    echo Install-name2:%_rpmdir/noarch/%name-devel-%version-%release.noarch.rpm > /dev/null
%else
    echo Install-name2:%_rpmdir/%_arch/%name-devel-%version-%release.%_arch.rpm > /dev/null
%endif

%if %{with debug}
    %global __os_install_post %nil
%endif

%install
umask 022
%if %{with static}
    make DESTDIR=%buildroot install
%else
    make DESTDIR=%buildroot DYNLIBS=1 install
%endif
chmod -R a+rX,u+w,go-w %buildroot

%files
%defattr(-,root,root)
%if %{with static}
    %_libdir/*.a
%else
    %exclude %_libdir/*.a
    %_libdir/*.%ver_major.%ver_minor.%ver_patch
    %_libdir/*.%ver_major.%ver_minor
%endif

%files devel
%dir %_includedir/%main_name
%_includedir/%main_name/*
%if ! %{with static}
    %_libdir/*.so
%endif

%files utils
%_bindir/*
%exclude %_bindir/tparser

%files -n %parser
%_bindir/tparser
