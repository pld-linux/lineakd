#
# Conditional build:
# _without_xosd	- without XOSD support
#
Summary:	Control multimedia keys on modern keyboards
Summary(pl):	Obs³uga klawiszy multimedialnych wystêpuj±cych na nowych klawiaturach
Name:		lineakd
Version:	0.7.2
Release:	1
License:	GPL
Group:		Applications/System
Source0:	http://dl.sourceforge.net/lineak/%{name}-%{version}.tar.gz
# Source0-md5:	986b947ce4f6e3dfa60fd66b4d26ea18
Patch0:		%{name}-achack.patch
Patch1:		%{name}-DESTDIR.patch
URL:		http://lineak.sourceforge.net/
BuildRequires:	XFree86-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
%{!?_without_xosd:BuildRequires:	xosd-devel}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Daemon to control the multimedia keys on modern keyboards.
Features X11 support, window manager independence, ability to
configure all keys (via GUI from separate package or .conf file),
volume control, and sound controls.

%description -l pl
Demon obs³uguj±cy klawisze multimedialne wystêpuj±ce na nowych
klawiaturach. Ma obs³ugê X11, jest niezale¿ny od zarz±dcy okien, daje
mo¿liwo¶æ konfiguracji wszystkich klawiszy (poprzez GUI z oddzielnego
pakietu lub plik .conf), sterowania g³o¶no¶ci± i d¼wiêkiem.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

# kill AC_PROG_LIBTOOL
head -n 4672 acinclude.m4 > acinclude.m4.tmp
mv -f acinclude.m4.tmp acinclude.m4

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?_without_xosd:--with-xosd}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README TODO
%attr(755,root,root) %{_bindir}/lineakd
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/lineakkb.def
