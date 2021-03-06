%define		gitver	%{nil}

Summary:	Userspace interface to kernel DRM services
Name:		libdrm
Version:	2.4.61
%if "%{gitver}" != "%{nil}"
Release:	0.%{gitver}.1
Source0:	http://cgit.freedesktop.org/mesa/drm/snapshot/drm-%{gitver}.tar.bz2
# Source0-md5:	a77a37370f6f8e17f5c4fe40b1b98782
%else
Release:	1
Source0:	http://dri.freedesktop.org/libdrm/%{name}-%{version}.tar.gz
# Source0-md5:	a77a37370f6f8e17f5c4fe40b1b98782
%endif
License:	MIT
Group:		Libraries
URL:		http://dri.freedesktop.org/
BuildRequires:	autoconf
BuildRequires:	automake
# just for tests
#BuildRequires:	cairo-devel
BuildRequires:	libpciaccess-devel
BuildRequires:	libtool
BuildRequires:	udev-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Userspace interface to kernel DRM services.

%package devel
Summary:	Header files for libdrm library
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	%{name}-intel = %{version}-%{release}
Requires:	%{name}-nouveau = %{version}-%{release}
Requires:	%{name}-radeon = %{version}-%{release}

%description devel
Header files for libdrm library.

%package intel
Summary:	DRM library for Intel GFX
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description intel
DRM library for Intel GFX.

%package nouveau
Summary:	DRM library for Nvidia (nouveau) GFX
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description nouveau
DRM library for Nvidia (nouveau) GFX.

%package radeon
Summary:	DRM library for ATI (radeon) GFX
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description radeon
DRM library for ATI (radeon) GFX.

%prep
%if "%{gitver}" != "%{nil}"
%setup -qn drm-%{gitver}
%else
%setup -q
%endif

# not required
%{__sed} -i "/pthread-stubs/d" configure.ac

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules	\
	--enable-manpages=no
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /usr/sbin/ldconfig
%postun	-p /usr/sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/libdrm.so.?
%attr(755,root,root) %ghost %{_libdir}/libkms.so.?
%attr(755,root,root) %{_libdir}/libdrm.so.*.*.*
%attr(755,root,root) %{_libdir}/libkms.so.*.*.*

%files intel
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/libdrm_intel.so.?
%attr(755,root,root) %{_libdir}/libdrm_intel.so.*.*.*

%files nouveau
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/libdrm_nouveau.so.?
%attr(755,root,root) %{_libdir}/libdrm_nouveau.so.*.*.*

%files radeon
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/libdrm_radeon.so.?
%attr(755,root,root) %{_libdir}/libdrm_radeon.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdrm*.so
%attr(755,root,root) %{_libdir}/libkms.so
%{_includedir}/*.h
%{_includedir}/libdrm
%{_includedir}/libkms
%{_pkgconfigdir}/*.pc

