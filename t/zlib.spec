Name:    zlib
Version: 1.3
Release: 5%{?dist}
Summary: Compression and decompression library
# /contrib/dotzlib/ have Boost license
License: zlib and Boost
URL: https://www.zlib.net/

Source: https://www.zlib.net/zlib-%{version}.tar.xz

BuildRequires: make
BuildRequires: automake, autoconf, libtool


%description
Zlib is a general-purpose, patent-free, lossless data compression
library which is used by many different programs.


%package devel
Summary: Header files and libraries for Zlib development
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
The zlib-devel package contains the header files and libraries needed
to develop programs that use the zlib compression and decompression
library.


%package static
Summary: Static libraries for Zlib development
Requires: %{name}-devel%{?_isa} = %{version}-%{release}

%description static
The zlib-static package includes static libraries needed
to develop programs that use the zlib compression and
decompression library.


%prep
%setup -q
iconv -f iso-8859-2 -t utf-8 < ChangeLog > ChangeLog.tmp
mv ChangeLog.tmp ChangeLog


%build
export CFLAGS="$RPM_OPT_FLAGS"

export LDFLAGS="$LDFLAGS -Wl,-z,relro -Wl,-z,now"
# no-autotools, %%configure is not compatible
%ifarch s390 s390x
  ./configure --libdir=%{_libdir} --includedir=%{_includedir} --prefix=%{_prefix} --dfltcc
%else
  ./configure --libdir=%{_libdir} --includedir=%{_includedir} --prefix=%{_prefix}
%endif
%make_build


%check
make test


%install
%make_install
find $RPM_BUILD_ROOT -name '*.la' -delete


%files
%license README
%doc ChangeLog FAQ
%{_libdir}/libz.so.*

%files devel
%doc doc/algorithm.txt test/example.c
%{_libdir}/libz.so
%{_libdir}/pkgconfig/zlib.pc
%{_includedir}/zlib.h
%{_includedir}/zconf.h
%{_mandir}/man3/zlib.3*

%files static
%license README
%{_libdir}/libz.a
