Summary:	Enhanced c-shell
Summary(de):	Erweiterte C-Shell
Summary(fr):	Shell C amélioré
Summary(pl):	Zaawansowany C-shell
Summary(tr):	Geliþmiþ c-kabuðu (c-shell)
Name:		tcsh
%define		ver	6.09
%define		sub_ver	00
Version:	%{ver}.%{sub_ver}
Release:	4
Copyright:	distributable
Group:		Shells
Group(pl):	Pow³oki
Source0:	ftp://ftp.astron.com/pub/tcsh/%{name}-%{ver}.tar.gz
Source1:	csh.cshrc
Source2:	tcsh-skel-.login
Patch0:		tcsh-utmp.patch
Patch1:		tcsh-security.patch
Patch2:		tcsh-misc.patch
Patch3:		tcsh-fhs.patch
Patch4:		tcsh-pathmax.patch
Patch5:		tcsh-strcoll.patch
Patch6:		tcsh-termios.patch
Provides:	csh
Prereq:		fileutils
Prereq:		grep
BuildRequires:	ncurses-devel >= 5.0
BuildRequires:	ncurses-static
BuildRequires:	glibc-static
Buildroot:	/tmp/%{name}-%{version}-root

%define		_bindir		/bin

%description
'tcsh' is an enhanced version of csh (the C shell), with additional features
such as command history, filename completion, and fancier prompts.

%description -l de
'tcsh' ist eine erweiterte Version von csh (der C-Shell) mit zusätzlichen
Funktionen wie Befehlsgeschichte, Dateinamenvervollständigung und
attraktiveren Prompts.

%description -l fr
'tcsh' est une version améliorée de csh (le shell C), avec des
fonctionnalités supplémentaires comme un historique des commandes,
la complétion des noms de fichiers, et des prompts sympas.

%description -l pl
Tcsh jest zaawansowanym wersj± shella csh (C-shell), z ró¿norodnymi 
udogodnieniami takimi jak historia komend itp.

%description -l tr
tcsh, csh'in (C kabuðu) geliþkin bir sürümüdür ve komut tarihçesi, dosya adý
tamamlama ve þýk komut imleri gibi özellikler sunar.

%package static
Summary:	Staticaly linked Enhanced c-shell
Summary(pl):	Statycznie zlinkowany zaawansowany C-shell
Group:		Shells
Group(pl):	Pow³oki
Requires:	%{name}

%description static
'tcsh' is an enhanced version of csh (the C shell), with additional features
such as command history, filename completion, and fancier prompts.

This packege contains staticly linked version of tcsh.

%description static -l pl
Tcsh jest zaawansowanym wersj± shella csh (C-shell), z ró¿norodnymi
udogodnieniami takimi jak historia komend itp.

W tym pakiecie jest statycznie zlinkowany tcsh.

%prep
%setup 	-q
%patch0 -p1 
%patch1 -p1 
%patch2 -p1 
%patch3	-p1
%patch4	-p1
%patch5	-p1
%patch6	-p1

%build
autoconf
%configure

make LDFLAGS="-static -s" LIBES="-ltinfo -lcrypt -lnsl"
mv tcsh tcsh.static
make LDFLAGS="-s" LIBES="-ltinfo -lcrypt -lnsl"

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/{etc/skel/C,%{_mandir}/man1,bin}
install tcsh tcsh.static $RPM_BUILD_ROOT%{_bindir}

install tcsh.man $RPM_BUILD_ROOT%{_mandir}/man1/tcsh.1
echo .so tcsh.1 > $RPM_BUILD_ROOT%{_mandir}/man1/csh.1

ln -sf tcsh $RPM_BUILD_ROOT%{_bindir}/csh
nroff -me eight-bit.me > eight-bit.txt

install %{SOURCE1} $RPM_BUILD_ROOT/etc
install %{SOURCE2} $RPM_BUILD_ROOT/etc/skel/C/.login

gzip -9fn $RPM_BUILD_ROOT%{_mandir}/man1/* \
	NewThings FAQ eight-bit.txt complete.tcsh

%post
if [ ! -f /etc/shells ]; then
	echo "%{_bindir}/tcsh" > /etc/shells
	echo "%{_bindir}/csh" >> /etc/shells
else
	grep '^%{_bindir}/tcsh$' /etc/shells > /dev/null || echo "%{_bindir}/tcsh" >> /etc/shells
	grep '^%{_bindir}/csh$' /etc/shells > /dev/null || echo "%{_bindir}/csh" >> /etc/shells
fi

%post static
if [ ! -f /etc/shells ]; then
	echo "%{_bindir}/tcsh.static" > /etc/shells
else
	grep '^%{_bindir}/tcsh.static$' /etc/shells > /dev/null || echo "%{_bindir}/tcsh.static" >> /etc/shells
fi

%postun
if [ ! -x %{_bindir}/tcsh ]; then
	grep -v '^%{_bindir}/tcsh$' /etc/shells | grep -v '^%{_bindir}/csh$'> /etc/shells.rpm
	mv /etc/shells.rpm /etc/shells
fi

%postun static
if [ ! -x %{_bindir}/tcsh.static ]; then
	grep -v '^%{_bindir}/tcsh.static$' /etc/shells > /etc/shells.rpm
	mv /etc/shells.rpm /etc/shells
fi

%files
%defattr(644,root,root,755)
%doc {NewThings,FAQ,eight-bit.txt,complete.tcsh}.gz

/etc/csh.*
/etc/skel/C/.login

%attr(755,root,root) %{_bindir}/csh
%attr(755,root,root) %{_bindir}/tcsh
%{_mandir}/man1/*

%clean
rm -rf $RPM_BUILD_ROOT

%files static
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/tcsh.static
