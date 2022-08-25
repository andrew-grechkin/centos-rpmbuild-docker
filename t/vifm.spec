%bcond_with     gtk
%bcond_without  libmagic
%bcond_with     x11

Name:           vifm
Version:        0.12
Release:        2%{?dist}
Summary:        File manager with curses interface, which provides Vi[m]-like environment

License:        GPLv2+
URL:            http://vifm.info/
Source0:        https://github.com/%{name}/%{name}/releases/download/v%{version}/%{name}-%{version}.tar.bz2

BuildRequires: make
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: desktop-file-utils
BuildRequires: gcc
BuildRequires: ncurses-devel
BuildRequires: perl-generators
%if %{with gtk}
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(gtk+-2.0)
%endif
%if %{with libmagic}
BuildRequires: file-devel
%endif
%if %{with x11}
BuildRequires: libX11-devel
%endif

%description
Vifm is a curses based vi[m] like file manager extended with some useful ideas
from mutt. If you use vi[m], vifm gives you complete keyboard control over
your files without having to learn a new set of commands. It goes not just
about vi[m] like keybindings, but also about modes, options, registers,
commands and other things you might already like in vi[m].

Just like vi[m], vifm tries to adhere to the Unix philosophy. So instead of
working solutions which are set in stone user is provided with a set of means
for customization of vifm to one's likings. Though builtin functionality
should be enough for most of use cases.


%prep
%autosetup -p1


%build
%configure \
%if %{with gtk}
    --with-gtk=yes \
%else
    --with-gtk=no \
%endif
%if %{with libmagic}
    --with-libmagic=yes \
%else
    --with-libmagic=no \
%endif
%if %{with x11}
    --with-X11=yes
%else
    --with-X11=no
%endif
%make_build


%install
%make_install

rm %{buildroot}%{_pkgdocdir}/COPYING


%check
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop


%files
%license COPYING
%{_bindir}/%{name}
%{_bindir}/%{name}-convert-dircolors
%{_bindir}/%{name}-pause
%{_bindir}/%{name}-screen-split
%{_datadir}/%{name}/
%{_datadir}/applications/*.desktop
%{_datadir}/bash-completion/completions/%{name}
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/zsh/site-functions/_%{name}
%{_mandir}/man1/*
%{_pkgdocdir}/
%{_sysconfdir}/%{name}/


%changelog
* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Sep 29 2021 Artem Polishchuk <ego.cordatus@gmail.com> - 0.12-1
- build(update): 0.12

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Sep 24 2020 Artem Polishchuk <ego.cordatus@gmail.com> - 0.11-1
- Update to 0.11

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Apr 06 2020 Artem Polishchuk <ego.cordatus@gmail.com> - 0.10.1-3
- Update package and fix FTBFS | RHBZ#1800234

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Oct 29 2019 Ben Boeckel <mathstuf@gmail.com> - 0.10.1-1
- Update to 0.10.1 (rhbz#1462578)
- Remove vifm-media-osx script

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jul 11 2019 Petr Pisar <ppisar@redhat.com> - 0.8.2-8
- Fix building with glibc 2.25 (bug #1606644)

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Jul 23 2016 Ben Boeckel <mathstuf@gmail.com> - 0.8.2-1
- update to 0.8.2

* Sat Apr 23 2016 Ben Boeckel <mathstuf@gmail.com> - 0.8.1a-1
- update to 0.8.1a

* Wed Mar 23 2016 Ralf CorsГ©pius <corsepiu@fedoraproject.org> - 0.8-3
- Install docs directly into %%{_pkgdocdir} (F24FTBFS, RHBZ#1308228).
- Add %%license.
- Modernize spec.

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Jul 19 2015 Ben Boeckel <mathstuf@gmail.com> - 0.8-1
- Update to 0.8

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Dec 10 2014 Ben Boeckel <mathstuf@gmail.com> - 0.7.8-1
- Update to 0.7.8

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Aug 08 2014 Yaakov Selkowitz <yselkowi@redhat.com> - 0.7.6-3
- Fix %%files for 0.7.6 (#1107084)

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Nov 20 2013 Ben Boeckel <mathstuf@gmail.com> - 0.7.6-1
- Update to 0.7.6

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu May 30 2013 Ben Boeckel <mathstuf@gmail.com> - 0.7.5-1
- Update to 0.7.5

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.4a-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Nov 04 2012 Ben Boeckel <mathstuf@gmail.com> - 0.7.4a-1
- Update to 0.7.4a

* Mon Jul 23 2012 Ben Boeckel <mathstuf@gmail.com> - 0.7.3a-1
- Update to 0.7.3a

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 24 2011 Ben Boeckel <mathstuf@gmail.com> - 0.6.2-1
- Update to 0.6.2
- Remove deletion patch (unable to reproduce original bug with new version)

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jun 19 2010 Pierre Dorbais <pierre.dorbais@free.fr> 0.5-4
- Add patch to fix crash when deleting four or more files (Bug #592725)

* Tue Apr 13 2010 Pierre Dorbais <pierre.dorbais@free.fr> 0.5-3
- Add dir macro to fix files listed twice
- Add blank lines between changelog entries

* Mon Apr 12 2010 Pierre Dorbais <pierre.dorbais@free.fr> 0.5-2
- Add INSTALL variable to make
- Add patch Patch0
- Add missing path to files macro
- Remove INSTALL doc file
- Remove BuildRoot tag

* Mon Feb 08 2010 Pierre Dorbais <pierre.dorbais@free.fr> 0.5-1
- Initial RPM release
