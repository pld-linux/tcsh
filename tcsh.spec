Summary:	Enhanced c-shell
Summary(de):	Erweiterte C-Shell
Summary(fr):	Shell C amélioré.
Summary(pl):	Zaawansowany C-shell -- wprawdzie nie tak jak bash ale ... ;)
Summary(tr):	Geliþmiþ c-kabuðu (c-shell)
Name:		tcsh
Version:	6.08.01
Release:	1
Copyright:	distributable
Group:		Shells
Source0:	ftp://ftp.ee.cornell.edu/pub/tcsh/%{name}-%{version}.tar.gz
Source1:	csh.cshrc
Patch0:		%{name}-utmp.patch
Patch1:		%{name}-security.patch
Patch2:		%{name}-misc.patch
Patch3:		%{name}-fhs.patch
Provides:	csh
Prereq:		fileutils
Prereq:		grep
Buildroot:	/tmp/%{name}-%{version}-root

%description
'tcsh' is an enhanced version of csh (the C shell), with additional features
such as command history, filename completion, and fancier prompts.

%description -l pl
Tcsh jest zaawansowanym wersj± shella csh (C-shell), z ró¿norodnymi 
udogodnieniami takimi jak historia komend itp.

%description -l de
'tcsh' ist eine erweiterte Version von csh (der C-Shell) mit zusätzlichen
Funktionen wie Befehlsgeschichte, Dateinamenvervollständigung und
attraktiveren Prompts.

%description -l fr
'tcsh' est une version améliorée de csh (le shell C), avec des
fonctionnalités supplémentaires comme un historique des commandes,
la complétion des noms de fichiers, et des prompts sympas.

%description -l tr
tcsh, csh'in (C kabuðu) geliþkin bir sürümüdür ve komut tarihçesi, dosya adý
tamamlama ve þýk komut imleri gibi özellikler sunar.

%prep
%setup 	-q -n %{name}-%{version}
%patch0 -p1 
%patch1 -p1 
%patch2 -p1 
%patch3	-p1

%build
autoconf
CFLAGS=$RPM_OPT_FLAGS \
    ./configure \
    --prefix=%{_prefix} \
    --datadir=%{_datadir} \
    %{_target_platform}

make 

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/{etc,%{_mandir}/man1,bin}
install -s tcsh $RPM_BUILD_ROOT/bin/tcsh

install tcsh.man $RPM_BUILD_ROOT%{_mandir}/man1/tcsh.1
echo .so tcsh.1 > $RPM_BUILD_ROOT%{_mandir}/man1/csh.1

ln -sf tcsh $RPM_BUILD_ROOT/bin/csh
nroff -me eight-bit.me > eight-bit.txt

install %{SOURCE1} $RPM_BUILD_ROOT/etc

gzip -9fn $RPM_BUILD_ROOT%{_mandir}/man1/* 
gzip -9fn NewThings FAQ eight-bit.txt complete.tcsh

%post
if [ ! -f /etc/shells ]; then
	echo "/bin/tcsh" > /etc/shells
	echo "/bin/csh" >> /etc/shells
else
	grep '^/bin/tcsh$' /etc/shells > /dev/null || echo "/bin/tcsh" >> /etc/shells
	grep '^/bin/csh$' /etc/shells > /dev/null || echo "/bin/csh" >> /etc/shells
fi

%postun
if [ ! -x /bin/tcsh ]; then
	grep -v '^/bin/tcsh$' /etc/shells | grep -v '^/bin/csh$'> /etc/shells.rpm
	mv /etc/shells.rpm /etc/shells
fi

%files
%defattr(644,root,root,755)
%doc {NewThings,FAQ,eight-bit.txt,complete.tcsh}.gz

/etc/csh.*
%attr(755,root,root) /bin/*
%{_mandir}/man1/*

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Sun Nov 08 1998 Wojtek ¦lusarczyk <wojtek@shadow.eu.org>
		  Tomek K³oczko <k³oczek@pld.org.pl>	
  [6.07.09-1d]
- updated to 6.07.09,
- moved /etc/csh.cshrc from setupt package to tcsh,
- minor changes.

* Tue Jun 30 1998 Wojtek ¦lusarczyk <wojtek@shadow.eu.org>
  [6.07-2d]
- build for PLD Tornado,
- translation modified for pl.
- start at RH spec file
