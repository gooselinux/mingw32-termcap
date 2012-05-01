# Note: Termcap was deprecated and removed from Fedora after F-8.  It
# has been replaced by ncurses.  However ncurses cannot be compiled on
# Windows so we have to supply termcap.  In addition, the last stand-
# alone Fedora termcap package was actually just /etc/termcap from
# ncurses.  So here we are using the GNU termcap library which is
# regretably GPL'd.

%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

Name:           mingw32-termcap
Version:        1.3.1
Release:        8%{?dist}.4
Summary:        MinGW terminal feature database


License:        GPLv2+
Group:          Development/Libraries
URL:            ftp://ftp.gnu.org/gnu/termcap/
Source0:        ftp://ftp.gnu.org/gnu/termcap/termcap-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 49
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils

BuildRequires:  autoconf


%description
This is the GNU termcap library -- a library of C functions that
enable programs to send control strings to terminals in a way
independent of the terminal type.  The GNU termcap library does not
place an arbitrary limit on the size of termcap entries, unlike most
other termcap libraries.

This package contains libraries and development tools for the MinGW
cross-compiled version.


%prep
%setup -q -n termcap-%{version}

# Packaged script doesn't understand --bindir, so rebuild:
autoconf


%build
%{_mingw32_configure}
make

# Build a shared library.  No need for -fPIC on Windows.
%{_mingw32_cc} -shared \
  -Wl,--out-implib,libtermcap.dll.a \
  -o libtermcap-0.dll \
  termcap.o tparam.o version.o


%install
rm -rf $RPM_BUILD_ROOT

make install \
  prefix=$RPM_BUILD_ROOT%{_mingw32_prefix} \
  exec_prefix=$RPM_BUILD_ROOT%{_mingw32_prefix} \
  oldincludedir=

# Move the shared library to the correct locations.
mkdir -p $RPM_BUILD_ROOT%{_mingw32_bindir}
install -m 0755 libtermcap-0.dll $RPM_BUILD_ROOT%{_mingw32_bindir}
install -m 0755 libtermcap.dll.a $RPM_BUILD_ROOT%{_mingw32_libdir}

# Don't want the static library, thank you.
rm $RPM_BUILD_ROOT%{_mingw32_libdir}/libtermcap.a

# Move the info files to the correct location.
mkdir -p $RPM_BUILD_ROOT%{_mingw32_infodir}
mv $RPM_BUILD_ROOT%{_mingw32_prefix}/info/* $RPM_BUILD_ROOT%{_mingw32_infodir}


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%doc COPYING
%{_mingw32_bindir}/libtermcap-0.dll
%{_mingw32_libdir}/libtermcap.dll.a
%{_mingw32_includedir}/termcap.h
# Note that we want the info files in this package because
# there is no equivalent native Fedora package.
%{_mingw32_infodir}/*


%changelog
* Mon Dec 27 2010 Andrew Beekhof <abeekhof@redhat.com> - 1.3.1-8.4
- Rebuild everything with gcc-4.4
  Related: rhbz#658833

* Fri Dec 24 2010 Andrew Beekhof <abeekhof@redhat.com> - 1.3.1-8.3
- The use of ExclusiveArch conflicts with noarch, using an alternate COLLECTION to limit builds
  Related: rhbz#658833

* Wed Dec 22 2010 Andrew Beekhof <abeekhof@redhat.com> - 1.3.1-8.2
- Only build mingw packages on x86_64
  Related: rhbz#658833

* Wed Dec 22 2010 Andrew Beekhof <abeekhof@redhat.com> - 1.3.1-8.1
- Bump the revision to avoid tag collision
  Related: rhbz#658833

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 20 2009 Richard W.M. Jones <rjones@redhat.com> - 1.3.1-6
- Rebuild for mingw32-gcc 4.4

* Fri Dec 19 2008 Richard W.M. Jones <rjones@redhat.com> - 1.3.1-5
- Added license file to doc section.

* Wed Nov 19 2008 Richard W.M. Jones <rjones@redhat.com> - 1.3.1-4
- Rerun autoconf because the standard configure doesn't know --bindir.
- Set exec_prefix during make install step.

* Fri Oct 31 2008 Richard W.M. Jones <rjones@redhat.com> - 1.3.1-3
- Fix so it builds a working DLL.

* Thu Sep 25 2008 Richard W.M. Jones <rjones@redhat.com> - 1.3.1-1
- Initial RPM release.
