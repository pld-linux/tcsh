Summary:	Enhanced c-shell
Summary(de):	Erweiterte C-Shell
Summary(fr):	Shell C am�lior�.
Summary(pl):	Zaawansowany C-shell
Summary(tr):	Geli�mi� c-kabu�u (c-shell)
Name:		tcsh
%define		ver	6.09
%define		sub_ver	00
Version:	%{ver}.%{sub_ver}
Release:	1
Copyright:	distributable
Group:		Shells
Group(pl):	Pow�oki
Source0:	ftp://ftp.astron.com/pub/tcsh/%{name}-%{ver}.tar.gz
Source1:	csh.cshrc
Source2:	tcsh-skel-.login
Patch0:		%{name}-utmp.patch
Patch1:		%{name}-security.patch
Patch2:		%{name}-misc.patch
Patch3:		%{name}-fhs.patch
Provides:	csh
Prereq:		fileutils
Prereq:		grep
BuildRequires:	ncurses-devel
BuildRequires:	ncurses-static
BuildRequires:	glibc-static
Buildroot:	/tmp/%{name}-%{version}-root

%description
'tcsh' is an enhanced version of csh (the C shell), with additional features
such as command history, filename completion, and fancier prompts.

%description -l de
'tcsh' ist eine erweiterte Version von csh (der C-Shell) mit zus�tzlichen
Funktionen wie Befehlsgeschichte, Dateinamenvervollst�ndigung und
attraktiveren Prompts.

%description -l fr
'tcsh' est une version am�lior�e de csh (le shell C), avec des
fonctionnalit�s suppl�mentaires comme un historique des commandes,
la compl�tion des noms de fichiers, et des prompts sympas.

%description -l pl
Tcsh jest zaawansowanym wersj� shella csh (C-shell), z r�norodnymi 
udogodnieniami takimi jak historia komend itp.

%description -l tr
tcsh, csh'in (C kabu�u) geli�kin bir s�r�m�d�r ve komut tarih�esi, dosya ad�
tamamlama ve ��k komut imleri gibi �zellikler sunar.

%package static
Summary:	Statcly linked Enhanced c-shell
Summary(pl):	Statycznie zlinkowany Zaawansowany C-shell
Group:		Shells
Group(pl):	Pow�oki
Requires:	%{name}

%description static
'tcsh' is an enhanced version of csh (the C shell), with additional features
such as command history, filename completion, and fancier prompts.

This packege contains staticly linked version of tcsh.

%description static -l pl
Tcsh jest zaawansowanym wersj� shella csh (C-shell), z r�norodnymi 
udogodnieniami takimi jak historia komend itp.

W tym pakiecie jest statycznie zlinkowany tcsh.

%prep
%setup 	-q
%patch0 -p1 
%patch1 -p1 
%patch2 -p1 
%patch3	-p1

%build
autoconf
%configure

make LDFLAGS="-static -s" LIBES="-lncurses -lcrypt"
mv tcsh tcsh.static
make LDFLAGS="-s" LIBES="-lncurses -lcrypt"

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/{etc/skel/C,%{_mandir}/man1,bin}
install tcsh tcsh.static $RPM_BUILD_ROOT/bin

install tcsh.man $RPM_BUILD_ROOT%{_mandir}/man1/tcsh.1
echo .so tcsh.1 > $RPM_BUILD_ROOT%{_mandir}/man1/csh.1

ln -sf tcsh $RPM_BUILD_ROOT/bin/csh
nroff -me eight-bit.me > eight-bit.txt

install %{SOURCE1} $RPM_BUILD_ROOT/etc
install %{SOURCE2} $RPM_BUILD_ROOT/etc/skel/C/.login

gzip -9fn $RPM_BUILD_ROOT%{_mandir}/man1/* \
	NewThings FAQ eight-bit.txt complete.tcsh

%post
if [ ! -f /etc/shells ]; then
	echo "/bin/tcsh" > /etc/shells
	echo "/bin/csh" >> /etc/shells
else
	grep '^/bin/tcsh$' /etc/shells > /dev/null || echo "/bin/tcsh" >> /etc/shells
	grep '^/bin/csh$' /etc/shells > /dev/null || echo "/bin/csh" >> /etc/shells
fi

%post static
if [ ! -f /etc/shells ]; then
	echo "/bin/tcsh.static" > /etc/shells
else
	grep '^/bin/tcsh.static$' /etc/shells > /dev/null || echo "/bin/tcsh.static" >> /etc/shells
fi

%postun
if [ ! -x /bin/tcsh ]; then
	grep -v '^/bin/tcsh$' /etc/shells | grep -v '^/bin/csh$'> /etc/shells.rpm
	mv /etc/shells.rpm /etc/shells
fi

%postun static
if [ ! -x /bin/tcsh.static ]; then
	grep -v '^/bin/tcsh.static$' /etc/shells > /etc/shells.rpm
	mv /etc/shells.rpm /etc/shells
fi

%files
%defattr(644,root,root,755)
%doc {NewThings,FAQ,eight-bit.txt,complete.tcsh}.gz

/etc/csh.*
/etc/skel/C/.login

%attr(755,root,root) /bin/csh
%attr(755,root,root) /bin/tcsh
%{_mandir}/man1/*

%clean
rm -rf $RPM_BUILD_ROOT

%files static
%defattr(644,root,root,755)
%attr(755,root,root) /bin/tcsh.static
