Summary: Tools for Linux kernel block layer cache
Name: bcache-tools
Version: 1.0.8
Release: 2
License: GPLv2
Group: System/Base
URL: http://bcache.evilpiepirate.org/
#VCS: https://github.com/g2p/bcache-tools.git
# git clone https://github.com/g2p/bcache-tools.git
# cd bcache-tools/
# git archive --format=tar --prefix=bcache-tools-1.0.8/ v1.0.8 | gzip > ../bcache-tools-1.0.8.tar.gz
Source0: %{name}-%{version}.tar.gz
# This part is a prerelease version obtained by https://gist.github.com/djwong/6343451:
# git clone https://gist.github.com/6343451.git
# cd 6343451/
# git archive --format=tar --prefix=bcache-status-20140220/ 6d278f9886ab5f64bd896080b1b543ba7ef6c7a6 | gzip > ../bcache-status-20140220.tar.gz
# see also http://article.gmane.org/gmane.linux.kernel.bcache.devel/1951
Source1: bcache-status-20140220.tar.gz
# bcache status not provided as a true package, so this is a self maintained
# man page for it
# http://article.gmane.org/gmane.linux.kernel.bcache.devel/1946
Patch0: %{name}-status-20160804-man.patch
# Process commandline arguments
Patch1: %{name}-1.0.8-cmdline.patch
# configure is not "Fedora compliant", do a small step in the
# right direction
Patch2: %{name}-20131018-fedconf.patch
# util-linux takes care of bcache superblock identification so we remove
# the probe-cache call (which is Fedora specific):
Patch3: %{name}-1.0.8-noprobe.2.patch
# the following fix is pending upstream
# gcc 5.1.1 apparently is more picky than Fedora 21 gcc
Patch4: bcache-tools-1.0.8-crc64.patch
# Fedora 23 uses python3 by default
Patch5: bcache-status-python3.patch
# Fix BZ#1360951 - this fix is python 3 only
Patch6: bcache-status-rootgc.patch

Requires: python
Conflicts: dracut < 034
BuildRequires:	pkgconfig(blkid)
BuildRequires:	pkgconfig(uuid)

%description
Bcache is a Linux kernel block layer cache. It allows one or more fast disk
drives such as flash-based solid state drives (SSDs) to act as a cache for
one or more slower hard disk drives.
This package contains the utilities for manipulating bcache.

%global _udevlibdir /lib/udev
%global dracutlibdir %{_prefix}/lib/dracut

%prep
%setup -q -n bcache-tools-%{version}
tar xzf %{SOURCE1} --strip-components=1
%patch0 -p1 -b .man
%patch1 -p1 -b .cmdline
%patch2 -p1 -b .fedconfmake
chmod +x configure
%patch3 -p1 -b .noprobe
%patch4 -p1 -b .crc64
%patch5 -p1 -b .python3
%patch6 -p1 -b .rootgc

%build
%configure
%make

%install
mkdir -p \
    %{buildroot}%{_sbindir} \
    %{buildroot}%{_mandir}/man8 \
    %{buildroot}%{_udevlibdir} \
    %{buildroot}%{_udevrulesdir} \
    %{buildroot}%{dracutlibdir}/modules.d

%make_install \
    INSTALL="install -p" \
    UDEVLIBDIR=%{_udevlibdir} \
    DRACUTLIBDIR=%{dracutlibdir} \
    MANDIR=%{_mandir}

# prevent complaints when checking for unpackaged files
rm %{buildroot}%{_udevlibdir}/probe-bcache
rm %{buildroot}%{_mandir}/man8/probe-bcache.8
rm %{buildroot}%{_prefix}/lib/initcpio/install/bcache
rm %{buildroot}%{_datarootdir}/initramfs-tools/hooks/bcache


install -p  -m 755 bcache-status %{buildroot}%{_sbindir}/bcache-status

%files
%doc README COPYING
%{_udevrulesdir}/*
%{_mandir}/man8/*
%{_udevlibdir}/bcache-register
%{_udevlibdir}/bcache-params
%{_sbindir}/bcache-super-show
%{_sbindir}/bcache-status
%{_sbindir}/make-bcache
%{dracutlibdir}/modules.d/90bcache
