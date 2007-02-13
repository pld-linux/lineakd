#
# TODO:
# - check for sigservs on startup
#
Summary:	Control multimedia keys on modern keyboards
Summary(pl.UTF-8):	Obsługa klawiszy multimedialnych występujących na nowych klawiaturach
Name:		lineakd
Version:	0.9
Release:	0.2
License:	GPL
Group:		Applications/System
Source0:	http://dl.sourceforge.net/lineak/%{name}-%{version}.tar.gz
# Source0-md5:	8a45672a6cea666873398ecc36a5070c
Patch0:		%{name}-make.patch
URL:		http://lineak.sourceforge.net/
BuildRequires:	autoconf >= 2.59-9
BuildRequires:	automake
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:1.5
BuildRequires:	xorg-lib-libXtst-devel
Requires:	%{name}-defs = %{version}-%{release}
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Daemon to control the multimedia keys on modern keyboards. Features
X11 support, window manager independence, ability to configure all
keys (via GUI from separate package or .conf file), volume control,
and sound controls.

%description -l pl.UTF-8
Demon obsługujący klawisze multimedialne występujące na nowych
klawiaturach. Ma obsługę X11, jest niezależny od zarządcy okien, daje
możliwość konfiguracji wszystkich klawiszy (poprzez GUI z oddzielnego
pakietu lub plik .conf), sterowania głośnością i dźwiękiem.

%package libs
Summary:	Lineak shared library
Summary(pl.UTF-8):	Biblioteka współdzielona lineak
Group:		Libraries

%description libs
Lineak shared library.

%description libs -l pl.UTF-8
Biblioteka współdzielona lineak.

%package devel
Summary:	Header files for lineak library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki lineak
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	libstdc++-devel
Requires:	xorg-lib-libX11-devel

%description devel
Header files for lineak library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki lineak.

%package static
Summary:	Static lineak library
Summary(pl.UTF-8):	Statyczna biblioteka lineak
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static lineak library.

%description static -l pl.UTF-8
Statyczna biblioteka lineak.

%package defs
Summary:	Keyboard definitions for lineakd
Summary(pl.UTF-8):	Definicje klawiatur dla lineakd
Group:		Applications/System
Conflicts:	lineakd < 0.7.2-4

%description defs
Keyboard definitions for lineakd.

%description defs -l pl.UTF-8
Definicje klawiatur dla lineakd.

%prep
%setup -q
%patch0 -p1

cat admin/{acinclude.m4.in,lineak.m4.in} > acinclude.m4

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README TODO lineakd.conf.example lineakd.conf.kde.example lineakkb.def.custom_example
%attr(755,root,root) %{_bindir}/*
%ifarch %{ix86} %{x8664} arm alpha
# these machines do have keyboard accessible through io ports
%attr(754,root,root) %{_sbindir}/send_to_keyboard
%endif
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/plugins
%{_mandir}/man1/lineakd.1*
%{_mandir}/man8/*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/liblineak.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/liblineak.so
%{_libdir}/liblineak.la
%{_includedir}/lineak

%files static
%defattr(644,root,root,755)
%{_libdir}/liblineak.a

%files defs
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lineakkb.def
