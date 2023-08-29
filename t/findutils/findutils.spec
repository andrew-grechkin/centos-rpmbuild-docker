%define _unpackaged_files_terminate_build 0

Summary: The GNU versions of find utilities (find and xargs)
Name: findutils
Version: 4.9.0
Release: 1%{?dist}
Epoch: 1
License: GPLv3+
Group: Applications/File
URL: http://www.gnu.org/software/findutils/
Source0: https://ftp.gnu.org/gnu/findutils/%{name}-%{version}.tar.xz

Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
Conflicts: filesystem < 3
Provides: /bin/find
Provides: bundled(gnulib)

Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: automake
BuildRequires: dejagnu
BuildRequires: gettext-devel
BuildRequires: libselinux-devel
BuildRequires: texinfo

%description
The findutils package contains programs which will help you locate
files on your system.  The find utility searches through a hierarchy
of directories looking for files which match a certain set of criteria
(such as a file name pattern).  The xargs utility builds and executes
command lines from standard input arguments (usually lists of file
names generated by the find command).

You should install findutils because it includes tools that are very
useful for finding things on your system.

%prep
%setup -q
#rm -rf locate

# needed because of findutils-4.4.0-no-locate.patch
#sed -e '/^SUBDIRS/s/locate//' -e 's/frcode locate updatedb//' -i Makefile.in
#autoreconf -ivf

%build
%configure

# uncomment to turn off optimizations
#find -name Makefile | xargs sed -i 's/-O2/-O0/'

make %{?_smp_mflags}

%check
make check

%install
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_infodir}/dir

%find_lang %{name}

%post
if [ -f %{_infodir}/find.info.gz ]; then
  /sbin/install-info %{_infodir}/find.info.gz %{_infodir}/dir || :
fi

%preun
if [ $1 = 0 ]; then
  if [ -f %{_infodir}/find.info.gz ]; then
    /sbin/install-info --delete %{_infodir}/find.info.gz %{_infodir}/dir || :
  fi
fi

%files -f %{name}.lang
%doc AUTHORS COPYING NEWS README THANKS TODO ChangeLog
%{_bindir}/find
%{_bindir}/xargs
%{_mandir}/man1/find.1*
%{_mandir}/man1/xargs.1*
%{_infodir}/find.info*
%{_infodir}/find-maint.info.gz
