Summary:	Compiler frontend for the W3C XML Schema definition language
Summary(pl.UTF-8):	Frontend kompilatora do języka definicji W3C XML Schema
Name:		libxsd-frontend
Version:	2.0.0
Release:	1
License:	GPL v2 + Xerces-C++ exception
Group:		Libraries
Source0:	https://www.codesynthesis.com/download/libxsd-frontend/2.0/%{name}-%{version}.tar.bz2
# Source0-md5:	040b40977ac8294e8591affe6061f68d
Source1:	https://www.codesynthesis.com/download/build/0.3/build-0.3.10.tar.bz2
# Source1-md5:	a7d2f4af455cb6c736c0fa02b10280f9
URL:		https://www.codesynthesis.com/projects/libxsd-frontend/
BuildRequires:	libcutl-devel >= 1.8.0
BuildRequires:	libstdc++-devel >= 5:3.4.3
BuildRequires:	xerces-c-devel >= 3.0.0
Requires:	libcutl >= 1.8.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libxsd-frontend is a compiler frontend for the W3C XML Schema
definition language. It includes parser, semantic graph types and
traversal mechanism.

%description -l pl.UTF-8
libxsd-frontend to frontend kompilatora do języka definicji W3C XML
Schema. Zawiera parser, typy grafów semantycznych oraz mechanizm
przechodzenia.

%package devel
Summary:	Header files for xsd-frontend library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki xsd-frontend
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel >= 5:3.4.3

%description devel
Header files for xsd-frontend library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki xsd-frontend.

%prep
%setup -q -a1

ln -sf build-0.3.10 build-0.3

install -d build/cxx/gnu build/ld
cat >build/cxx/configuration-dynamic.make <<EOF
cxx_id       := gnu
cxx_optimize := y
cxx_debug    := n
cxx_rpath    := n
cxx_pp_extra_options := %{rpmcppflags}
cxx_extra_options    :=
cxx_ld_extra_options := %{rpmldflags}
cxx_extra_libs       :=  -lxerces-c
cxx_extra_lib_paths  := 
EOF

cat >build/cxx/gnu/configuration-dynamic.make <<EOF
cxx_gnu := %{__cxx}
cxx_gnu_standard := gnu++11
cxx_gnu_libraries :=
cxx_gnu_optimization_options := %{rpmcxxflags}
# seem not needed
#cxx_gnu_target := i686-pld-linux-gnu
#cxx_gnu_target_cpu := i686
#cxx_gnu_target_mf := pld
#cxx_gnu_target_kernel := linux
#cxx_gnu_target_os := gnu
EOF

cat >build/ld/configuration-lib-dynamic.make <<EOF
ld_lib_type := shared
EOF

cat >build/import/libcutl/configuration-dynamic.make <<EOF
libcutl_installed := y
EOF

cat >build/import/libxerces-c/configuration-dynamic.make <<EOF
libcutl_installed := y
EOF

%build
%{__make} \
	build=$(pwd)/build-0.3/build \
	verbose=1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_includedir}/xsd-frontend/{generators,semantic-graph,transformations,traversal},%{_libdir}}

install xsd-frontend/libxsd-frontend.so $RPM_BUILD_ROOT%{_libdir}
cp -p xsd-frontend/*.hxx $RPM_BUILD_ROOT%{_includedir}/xsd-frontend
cp -p xsd-frontend/generators/*.hxx $RPM_BUILD_ROOT%{_includedir}/xsd-frontend/generators
cp -p xsd-frontend/semantic-graph/*.hxx $RPM_BUILD_ROOT%{_includedir}/xsd-frontend/semantic-graph
cp -p xsd-frontend/transformations/*.hxx $RPM_BUILD_ROOT%{_includedir}/xsd-frontend/transformations
cp -p xsd-frontend/traversal/*.hxx $RPM_BUILD_ROOT%{_includedir}/xsd-frontend/traversal

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE NEWS README
%attr(755,root,root) %{_libdir}/libxsd-frontend.so

%files devel
%defattr(644,root,root,755)
%{_includedir}/xsd-frontend
