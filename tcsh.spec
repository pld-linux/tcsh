#
# Conditional build:
%bcond_with	working_history	# compiles tcsh with timestamps in
				# ~/.history file so it serves any real purpose (which
				# is not the case for default PLD tcsh)
%bcond_without	static		# don't build static version
#
Summary:	Enhanced c-shell
Summary(de):	Erweiterte C-Shell
Summary(es):	C-shell mejorada
Summary(fr):	Shell C amélioré
Summary(ko):	cshÀÇ Çâ»óµÈ ¹öÀü
Summary(pl):	Zaawansowany C-shell
Summary(pt_BR):	C-shell melhorada
Summary(ru):	õÌÕÞÛÅÎÁÑ ×ÅÒÓÉÑ csh
Summary(tr):	Geliþmiþ c-kabuðu (c-shell)
Summary(uk):	ðÏËÒÁÝÅÎÁ ×ÅÒÓÑ csh
Name:		tcsh
Version:	6.13.00
Release:	3
License:	distributable
Group:		Applications/Shells
Source0:	ftp://ftp.astron.com/pub/tcsh/%{name}-%{version}.tar.gz
# Source0-md5:	11c0c9c9148652dc01270c4880d1cc6e
Source1:	csh.cshrc
Source2:	csh.login
Source3:	%{name}-skel-.login
Patch0:		%{name}-utmp.patch
Patch1:		%{name}-misc.patch
Patch2:		%{name}-termios.patch
Patch3:		%{name}-no-timestamp-history.patch
Patch4:		%{name}-no_stat_utmp.patch
Patch5:		%{name}-time.patch
Patch6:		%{name}-rlimit_locks.patch
Patch7:		%{name}-dspmbyte.patch
Patch8:		%{name}-no_TERMCAP.patch
Patch9:		%{name}-nls-codesets.patch
Patch10:	%{name}-sysmalloc.patch
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	groff
# for gencat
BuildRequires:	iconv
BuildRequires:	ncurses-devel >= 5.0
%if %{with static}
BuildRequires:	glibc-static
BuildRequires:	ncurses-static
%endif
Requires(post,preun):	grep
Requires(preun):	fileutils
Provides:	csh
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

%description -l es
"tcsh" es una versión mejorada de la csh (C shell), con
características adicionales como historia de los comandos, complemento
de nombre de archivo y prompts.

%description -l fr
'tcsh' est une version améliorée de csh (le shell C), avec des
fonctionnalités supplémentaires comme un historique des commandes, la
complétion des noms de fichiers, et des prompts sympas.

%description -l pl
Tcsh jest zaawansowan± wersj± pow³oki csh (C-shell), z ró¿norodnymi
udogodnieniami takimi jak historia komend itp.

%description -l pt_BR
"tcsh" é uma versão melhorada da csh (C shell), com características
adicionais como history dos comandos, complemento de nome de arquivo e
prompts.

%description -l ru
üÔÏ ÕÌÕÞÛÅÎÎÁÑ ×ÅÒÓÉÑ csh (the C shell) Ó ÄÏÐÏÌÎÉÔÅÌØÎÙÍÉ
×ÏÚÍÏÖÎÏÓÔÑÍÉ, ÔÁËÉÍÉ ËÁË ÉÓÔÏÒÉÑ ËÏÍÍÁÎÄ, ÄÏÐÏÌÎÅÎÉÅ ÉÍÅÎ ÆÁÊÌÏ× É
Ô.Ä.

%description -l tr
tcsh, csh'in (C kabuðu) geliþkin bir sürümüdür ve komut tarihçesi,
dosya adý tamamlama ve þýk komut imleri gibi özellikler sunar.

%description -l uk
ãÅ ÐÏËÒÁÝÅÎÁ ×ÅÒÓ¦Ñ csh (the C shell) Ú ÄÏÄÁÔËÏ×ÉÍÉ ÍÏÖÌÉ×ÏÓÔÑÍÉ,
ÔÁËÉÍÉ ÑË ¦ÓÔÏÒ¦Ñ ËÏÍÁÎÄ, ÚÁ×ÅÒÛÅÎÎÑ ¦ÍÅÎ ÆÁÊÌ¦× ¦ Ô.¦.

%package static
Summary:	Statically linked Enhanced c-shell
Summary(pl):	Skonsolidowana statycznie zaawansowana pow³oka C
Group:		Applications/Shells
Requires(post,preun):	grep
Requires(preun):	fileutils
Requires:	%{name} = %{version}-%{release}

%description static
'tcsh' is an enhanced version of csh (the C shell), with additional
features such as command history, filename completion, and fancier
prompts.

This packege contains statically linked version of tcsh.

%description static -l pl
Tcsh jest zaawansowan± wersj± pow³oki csh (C-shell), z ró¿norodnymi
udogodnieniami takimi jak historia komend itp.

W tym pakiecie jest statycznie skonsolidowany tcsh.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2	-p1
%{!?with_working_history:%patch3 -p1}
%patch4	-p1
%patch5	-p1
%patch6	-p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1

%build
cp /usr/share/automake/config.sub .
%{__aclocal}
%{__autoconf}
%configure
%if %{with static}
%{__make} \
	LDFLAGS="-static %{rpmldflags}" \
	LIBES="-ltinfo -lcrypt"
mv -f tcsh tcsh.static
%endif
%{__make} \
	LDFLAGS="%{rpmldflags}" \
	LIBES="-ltinfo -lcrypt"

%{__make} -C nls

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/skel,%{_mandir}/man1,%{_bindir}} \
	$RPM_BUILD_ROOT%{_datadir}/locale/{el,es,fr,it,ja}

%if %{with static}
install tcsh.static $RPM_BUILD_ROOT%{_bindir}
%endif
install tcsh $RPM_BUILD_ROOT%{_bindir}

install tcsh.man $RPM_BUILD_ROOT%{_mandir}/man1/tcsh.1
echo .so tcsh.1 > $RPM_BUILD_ROOT%{_mandir}/man1/csh.1

ln -sf tcsh $RPM_BUILD_ROOT%{_bindir}/csh
nroff -me eight-bit.me > eight-bit.txt

install %{SOURCE1} %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}
install %{SOURCE3} $RPM_BUILD_ROOT/etc/skel/.login

install tcsh.french.cat $RPM_BUILD_ROOT%{_datadir}/locale/fr/tcsh
install tcsh.italian.cat $RPM_BUILD_ROOT%{_datadir}/locale/it/tcsh
install tcsh.ja.cat $RPM_BUILD_ROOT%{_datadir}/locale/ja/tcsh
install tcsh.greek.cat $RPM_BUILD_ROOT%{_datadir}/locale/el/tcsh
install tcsh.spanish.cat $RPM_BUILD_ROOT%{_datadir}/locale/es/tcsh

%clean
rm -rf $RPM_BUILD_ROOT

%post
umask 022
if [ ! -f /etc/shells ]; then
	echo "%{_bindir}/tcsh" > /etc/shells
	echo "%{_bindir}/csh" >> /etc/shells
else
	grep -q '^%{_bindir}/tcsh$' /etc/shells || echo "%{_bindir}/tcsh" >> /etc/shells
	grep -q '^%{_bindir}/csh$' /etc/shells || echo "%{_bindir}/csh" >> /etc/shells
fi

%preun
umask 022
if [ "$1" = "0" ]; then
	grep -v '^%{_bindir}/t\?csh$' /etc/shells > /etc/shells.new
	mv -f /etc/shells.new /etc/shells
fi

%post static
umask 022
if [ ! -f /etc/shells ]; then
	echo "%{_bindir}/tcsh.static" > /etc/shells
else
	grep -q '^%{_bindir}/tcsh\.static$' /etc/shells || echo "%{_bindir}/tcsh.static" >> /etc/shells
fi

%preun static
umask 022
if [ "$1" = "0" ]; then
	grep -v '^%{_bindir}/tcsh\.static$' /etc/shells > /etc/shells.new
	mv -f /etc/shells.new /etc/shells
fi

%files
%defattr(644,root,root,755)
%doc NewThings FAQ eight-bit.txt complete.tcsh

%config(noreplace,missingok) %verify(not md5 mtime size) %{_sysconfdir}/csh.*
%config(noreplace,missingok) %verify(not md5 mtime size) /etc/skel/.login

%attr(755,root,root) %{_bindir}/csh
%attr(755,root,root) %{_bindir}/tcsh
%lang(fr) %{_datadir}/locale/fr/tcsh
%lang(it) %{_datadir}/locale/it/tcsh
%lang(ja) %{_datadir}/locale/ja/tcsh
%lang(el) %{_datadir}/locale/el/tcsh
%lang(es) %{_datadir}/locale/es/tcsh
%{_mandir}/man1/*

%if %{with static}
%files static
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/tcsh.static
%endif
