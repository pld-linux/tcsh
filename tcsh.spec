Summary:	Enhanced c-shell
Summary(de):	Erweiterte C-Shell
Summary(fr):	Shell C amélioré
Summary(pl):	Zaawansowany C-shell
Summary(tr):	Geliþmiþ c-kabuðu (c-shell)
Name:		tcsh
Version:	6.10.02
Release:	1
License:	distributable
Group:		Applications/Shells
Source0:	ftp://ftp.fujitsu.co.jp/pub/misc/shells/tcsh/%{name}-%{version}.tgz
Source1:	csh.cshrc
Source2:	%{name}-skel-.login
Patch0:		%{name}-utmp.patch
Patch1:		%{name}-misc.patch
Patch2:		%{name}-fhs.patch
Patch3:		%{name}-termios.patch
Patch4:		%{name}-no-timestamp-history.patch
Patch5:		%{name}-no_stat_utmp.patch
Patch6:		%{name}-locale.patch
Patch7:		%{name}-time.patch
Patch8:		%{name}-login.patch
Patch9:		%{name}-rlimit_locks.patch
Patch10:	%{name}-dspmbyte.patch
Provides:	csh
Prereq:		fileutils
Prereq:		grep
BuildRequires:	autoconf
BuildRequires:	ncurses-devel >= 5.0
BuildRequires:	ncurses-static
BuildRequires:	glibc-static
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_bindir		/bin

%description
'tcsh' is an enhanced version of csh (the C shell), with additional
features such as command history, filename completion, and fancier
prompts.

%description -l de
'tcsh' ist eine erweiterte Version von csh (der C-Shell) mit
zusätzlichen Funktionen wie Befehlsgeschichte,
Dateinamenvervollständigung und attraktiveren Prompts.

%description -l fr
'tcsh' est une version améliorée de csh (le shell C), avec des
fonctionnalités supplémentaires comme un historique des commandes, la
complétion des noms de fichiers, et des prompts sympas.

%description -l pl
Tcsh jest zaawansowanym wersj± shella csh (C-shell), z ró¿norodnymi
udogodnieniami takimi jak historia komend itp.

%description -l tr
tcsh, csh'in (C kabuðu) geliþkin bir sürümüdür ve komut tarihçesi,
dosya adý tamamlama ve þýk komut imleri gibi özellikler sunar.

%package static
Summary:	Statically linked Enhanced c-shell
Summary(pl):	Statycznie zlinkowany zaawansowany C-shell
Group:		Applications/Shells
Requires:	%{name}

%description static
'tcsh' is an enhanced version of csh (the C shell), with additional
features such as command history, filename completion, and fancier
prompts.

This packege contains statically linked version of tcsh.

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
%patch7	-p1
%patch8	-p1
%patch9	-p1
#%patch10 -p1

%build
%{__autoconf}
%configure

%{__make} LDFLAGS="-static %{rpmldflags}" LIBES="-ltinfo -lcrypt"
mv -f tcsh tcsh.static
%{__make} LDFLAGS="%{rpmldflags}" LIBES="-ltinfo -lcrypt"

%{__make} -C nls

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/{etc/skel,%{_mandir}/man1,%{_bindir}} \
	$RPM_BUILD_ROOT%{_datadir}/locale/{fr,it,ja,gr,es}

install tcsh tcsh.static $RPM_BUILD_ROOT%{_bindir}

install tcsh.man $RPM_BUILD_ROOT%{_mandir}/man1/tcsh.1
echo .so tcsh.1 > $RPM_BUILD_ROOT%{_mandir}/man1/csh.1

ln -sf tcsh $RPM_BUILD_ROOT%{_bindir}/csh
nroff -me eight-bit.me > eight-bit.txt

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/skel/.login

install tcsh.french.cat $RPM_BUILD_ROOT%{_datadir}/locale/fr/tcsh
install tcsh.italian.cat $RPM_BUILD_ROOT%{_datadir}/locale/it/tcsh
install tcsh.ja.cat $RPM_BUILD_ROOT%{_datadir}/locale/ja/tcsh
install tcsh.greek.cat $RPM_BUILD_ROOT%{_datadir}/locale/gr/tcsh
install tcsh.spanish.cat $RPM_BUILD_ROOT%{_datadir}/locale/es/tcsh

gzip -9nf NewThings FAQ eight-bit.txt complete.tcsh

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ ! -f /etc/shells ]; then
	echo "%{_bindir}/tcsh" > /etc/shells
	echo "%{_bindir}/csh" >> /etc/shells
else
	grep -q '^%{_bindir}/tcsh$' /etc/shells || echo "%{_bindir}/tcsh" >> /etc/shells
	grep -q '^%{_bindir}/csh$' /etc/shells || echo "%{_bindir}/csh" >> /etc/shells
fi

%post static
if [ ! -f /etc/shells ]; then
	echo "%{_bindir}/tcsh.static" > /etc/shells
else
	grep -q '^%{_bindir}/tcsh\.static$' /etc/shells || echo "%{_bindir}/tcsh.static" >> /etc/shells
fi

%preun
if [ "$1" = "0" ]; then
	grep -v '^%{_bindir}/t\?csh$' /etc/shells > /etc/shells.new
	mv -f /etc/shells.new /etc/shells
fi

%preun static
if [ "$1" = "0" ]; then
	grep -v '^%{_bindir}/tcsh\.static$' /etc/shells > /etc/shells.new
	mv -f /etc/shells.new /etc/shells
fi

%files
%defattr(644,root,root,755)
%doc {NewThings,FAQ,eight-bit.txt,complete.tcsh}.gz

%{_sysconfdir}/csh.*
/etc/skel/.login

%attr(755,root,root) %{_bindir}/csh
%attr(755,root,root) %{_bindir}/tcsh
%lang(fr) %{_datadir}/locale/fr/tcsh
%lang(it) %{_datadir}/locale/it/tcsh
%lang(ja) %{_datadir}/locale/ja/tcsh
%lang(gr) %{_datadir}/locale/gr/tcsh
%lang(es) %{_datadir}/locale/es/tcsh
%{_mandir}/man1/*

%files static
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/tcsh.static
