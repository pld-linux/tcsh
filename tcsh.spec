Summary:     Enhanced c-shell
Summary(de): Erweiterte C-Shell
Summary(fr): Shell C amélioré.
Summary(pl): Zaawansowany C-shell
Summary(tr): Geliþmiþ c-kabuðu (c-shell)
Name:        tcsh
%define majorversion 6.08
%define minorversion 00
Version:     %{majorversion}.%{minorversion}
Release:     1
Copyright:   distributable
Group:       Shells
Source0:     ftp://ftp.primate.wisc.edu/software/csh-tcsh-book/%{name}-%{majorversion}.tar.gz
Source1:     csh.cshrc
Patch0:      tcsh-utmp.patch
Patch1:      tcsh-termios.patch
Patch2:      tcsh-security.patch
Provides:    csh
Prereq:      fileutils grep
URL:         http://www.primate.wisc.edu/software/csh-tcsh-book/
Buildroot:   /tmp/%{name}-%{version}-root

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
Tcsh jest zaawansowan± wersj± shella csh (C-shell), z ró¿norodnymi 
udogodnieniami takimi jak historia komend itp.

%description -l tr
tcsh, csh'in (C kabuðu) geliþkin bir sürümüdür ve komut tarihçesi, dosya adý
tamamlama ve þýk komut imleri gibi özellikler sunar.

%prep
%setup -q
%patch0 -p1 -b .getutent
%patch1 -p1 -b .termios
%patch2 -p1 -b .security

%build
%configure
make LIBES="-lnsl -lncurses -lcrypt" DESTBIN="/bin"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/{bin,etc,usr/man/man1}

install -s tcsh $RPM_BUILD_ROOT/bin/tcsh
install tcsh.man $RPM_BUILD_ROOT%{_mandir}/man1/tcsh.1

ln -sf tcsh $RPM_BUILD_ROOT/bin/csh
echo .so tcsh.1 > $RPM_BUILD_ROOT%{_mandir}/man1/csh.1

nroff -me eight-bit.me > eight-bit.txt

install %{SOURCE1} $RPM_BUILD_ROOT/etc/

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ ! -f /etc/shells ]; then
	echo "/bin/tcsh" > /etc/shells
	echo "/bin/csh" > /etc/shells
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
%doc NewThings FAQ eight-bit.txt complete.tcsh
/etc/csh.cshrc
%attr(755,root,root) /bin/*
%{_mandir}/man1/*

%changelog
* Mon Nov 16 1998 Tomasz K³oczko <kloczek@rudy.mif.pg.gda.pl>
  [6.08.00-1]
- /etc/csh.cshrc moved from setup,
- use -lncurses which is now in /lib.

* Wed Aug  5 1998 Jeff Johnson <jbj@redhat.com>
- use -ltermcap so that /bin/tcsh can be used in single user mode w/o /usr.
- update url's

* Tue Jun 30 1998 Wojtek ¦lusarczyk <wojtek@shadow.eu.org>
- added pl translation.

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Oct 21 1997 Cristian Gafton <gafton@redhat.com>
- updated to 6.07; added BuildRoot
- cleaned up the spec file; fixed source url

* Wed Sep 03 1997 Erik Troan <ewt@redhat.com>
- added termios hacks for new glibc
- added /bin/csh to file list

* Fri Jun 13 1997 Erik Troan <ewt@redhat.com>
- built against glibc

* Fri Feb 07 1997 Erik Troan <ewt@redhat.com>
- Provides csh, adds and removes /bin/csh from /etc/shells if csh package
  isn't installed.
