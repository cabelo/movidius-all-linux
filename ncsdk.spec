#
# spec file for package modoki
#
# Copyright (c) 2017 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

Name:           ncsdk
Version:        1.12.00
Release:        1.1
License:        Intel-License
Packager:   Alessandro de Oliveira Faria (A.K.A CABELO) <cabelo@opensuse.org>
Summary: Library Intel Movidius Neural Compute SDK 
URL: https://www.movidius.com/
Source0:         %{name}-%{version}.tar.gz
Group: Productivity/Networking/Web/Servers
#BuildRequires: fdupes
BuildRoot: %{_tmppath}/%{name}-%{version}-build
BuildRequires: -post-build-checks -rpmlint-Factory -rpmlint-mini  -rpmlint
BuildRequires: gcc-c++, make, libcurl-devel, automake,  python, udev
%if 0%{?mageia}
BuildRequires:  libcryptopp-devel
%else
BuildRequires: libgcrypt-devel
%endif

%if 0%{?fedora} || 0%{?suse_version} || 0%{?sles_version}
BuildRequires: python3
%endif

%if 0%{?suse_version} || 0%{?sles_version}
BuildRequires: libusb-1_0-devel 
%else
BuildRequires: libusbx-devel 
%endif
  
%description
This Intel® Movidius™ Neural Compute software developer kit (NCSDK) is provided for users of the Intel® Movidius™ Neural Compute Stick (Intel® Movidius™ NCS). It includes software tools, an API, and examples, so developers can create software that takes advantage of the accelerated neural network capability provided by the Intel Movidius NCS hardware.

%package devel
Summary:        Devel package Intel Movidius Neural Compute SDK
Group:          Development/Libraries/C and C++
Requires:       ncsdk 
%if 0%{?fedora} || 0%{?suse_version} || 0%{?sles_version}
Requires:       python3
%endif

%description devel
This Intel® Movidius™ Neural Compute software developer kit (NCSDK) is provided for users of the Intel® Movidius™ Neural Compute Stick (Intel® Movidius™ NCS). It includes software tools, an API, and examples, so developers can create software that takes advantage of the accelerated neural network capability provided by the Intel Movidius NCS hardware.

%prep
#cd $RPM_SOURCE_DIR
#if [ -s %{name}.tar.gz ] ; then
#	if [ -d %{name} ] ; then rm -rf %{name} ; fi
#	tar zxf %{name}.tar.gz
#else
#	if [ -f %{name}-git.tar.gz ] ; then
#		if [ -d %{name} ] ; then rm -rf ncsdk ; fi
#		mkdir %{name}
#		cd %{name}
#		tar zxf ../%{name}-git.tar.gz --strip=1
#	elif [ -d %{name} ] ; then
#		cd %{name}
#		git pull
#		cd ..
#	else
#		git clone https://github.com/movidius/ncsdk
#	fi
#fi

%setup -q

%build
export CFLAGS="%{optflags} $(getconf LFS_CFLAGS)"
export CXXFLAGS="%{optflags} $(getconf LFS_CFLAGS)"
cd api/src/
make %{?_smp_mflags}

%install
mkdir -p %{buildroot}/usr/local/bin
mv ncsdk %{buildroot}/usr/local/bin
cd api/src/
make DESTDIR=%{buildroot} basicinstall 
make DESTDIR=%{buildroot} pythoninstall
mv %{buildroot}/usr/local/lib %{buildroot}/usr/local/lib64
#%if 0%{?fedora} || 0%{?suse_version} || 0%{?sles_version}
#ls -l
#%else
%if 0%{?rhel_version} || 0%{?centos_version} || 0%{?scientificlinux_version} ||  0%{?mdkversion}
/usr/bin/echo "PASSEI AQUI 00001-1"
/usr/bin/rm -rf %{buildroot}/usr/lib64/python3*
/usr/bin/rm -rf %{buildroot}/mvnc/
%else
/usr/bin/echo "PASSEI AQUI 00001-2"
%endif
find  %{buildroot}

%files
%{_prefix}/local/bin/ncsdk/*
%{_prefix}/local/lib64/*.so
%{_prefix}/local/lib64/*.so.*
%{_prefix}/local/lib64/mvnc/*
%if 0%{?rhel_version} || 0%{?centos_version} || 0%{?scientificlinux_version} ||  0%{?mdkversion}
%else
%{_prefix}/lib64/python3*/site-packages/mvnc/*
%endif
%{_prefix}/lib64/python2*/site-packages/mvnc/*
%{_sysconfdir}/udev/rules.d/97-usbboot.rules


%files devel
%{_prefix}/local/include/*

%clean

%post
/usr/bin/ln -s /usr/local/bin/ncsdk/mvNCCheck.py   /usr/local/bin/mvNCCheck
/usr/bin/ln -s /usr/local/bin/ncsdk/mvNCProfile.py /usr/local/bin/mvNCProfile
/usr/bin/ln -s /usr/local/bin/ncsdk/mvNCCompile.py /usr/local/bin/mvNCCompile
/usr/bin/udevadm control --reload-rules
/usr/bin/udevadm trigger
/sbin/ldconfig


%postun
/sbin/ldconfig
rm -rf /usr/local/bin/ncsdk
rm /usr/local/bin/mvNCCheck
rm /usr/local/bin/mvNCProfile
rm /usr/local/bin/mvNCCompile

%changelog
* Tue Sep 16 2016 - cabelo (at) opensuse.org 12.0.90
- Initial version


