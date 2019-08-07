#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries
%bcond_without	opencl		# OpenCL features
#
Summary:	Open-source decoder of AVS2-P2/IEEE1857.4 video coding standard
Summary(pl.UTF-8):	Dekoder standardu kodowania obrazu AVS2-P2/IEEE1857.4 o otwartych źródłach
Name:		davs2
Version:	1.6
Release:	2
License:	GPL v2+
Group:		Libraries
#Source0Download: https://github.com/pkuvcl/davs2/releases
Source0:	https://github.com/pkuvcl/davs2/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	c8861c1220c05a172b9ce472cbf929af
Patch0:		%{name}-extern.patch
Patch1:		%{name}-gcc8-fix.patch
Patch2:		%{name}-opt.patch
URL:		https://github.com/pkuvcl/davs2
%{?with_opencl:BuildRequires:	OpenCL-devel}
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.674
BuildRequires:	sed >= 4.0
%ifarch %{ix86} %{x8664}
BuildRequires:	yasm >= 1.2.0
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Open-source decoder of AVS2-P2/IEEE1857.4 video coding standard.

%description -l pl.UTF-8
Dekoder standardu kodowania obrazu AVS2-P2/IEEE1857.4 o otwartych
źródłach.

%package devel
Summary:	Header files for davs2 library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki davs2
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for davs2 library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki davs2.

%package static
Summary:	Static davs2 library
Summary(pl.UTF-8):	Statyczna biblioteka davs2
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static davs2 library.

%description static -l pl.UTF-8
Statyczna biblioteka davs2.

%prep
%setup -q
%patch0 -p1

%undos source/common/vec/intrinsic_{deblock_avx2,idct_avx2,inter_pred,inter_pred_avx2,intra-pred_avx2,pixel_avx,sao_avx2}.cc
%patch1 -p1
%patch2 -p1

%build
cd build/linux
# not autoconf configure
CC="%{__cc}" \
CXX="%{__cxx}" \
CFLAGS="%{rpmcflags}" \
CXXFLAGS="%{rpmcxxflags}" \
CPPFLAGS="%{rpmcppflags}" \
LDFLAGS="%{rpmldflags} -Wl,-z,noexecstack" \
./configure \
	--prefix=%{_prefix} \
	--bindir=%{_bindir} \
	--includedir=%{_includedir} \
	--libdir=%{_libdir} \
%ifarch x32
	--disable-asm \
%endif
	%{!?with_opencl:--disable-opencl} \
	--enable-pic \
	--enable-shared \
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build/linux install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md
%lang(zh) %doc README.zh.md
%attr(755,root,root) %{_bindir}/davs2
%attr(755,root,root) %{_libdir}/libdavs2.so.16

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdavs2.so
%{_includedir}/davs2.h
%{_includedir}/davs2_config.h
%{_pkgconfigdir}/davs2.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libdavs2.a
%endif
