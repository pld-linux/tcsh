# /etc/cshrc

# System wide environment and startup programs for csh users

setenv PATH "${PATH}:/usr/X11R6/bin"

[ `id -gn` = `id -un` -a `id -u` -gt 14 ]
if $status then
	umask 022
else
	umask 002
endif

setenv HOSTNAME `/bin/hostname`
set histfile="$HOME/.history"
set history=1000
set savehist=1000

foreach i ( /etc/env.d/* )
	set NAME=`basename $i`
	switch ( $NAME )
	  case *~:
	  case *.bak:
	  case *.rpmnew:
	  case *.rpmsave:
		# nothing
		breaksw
	  default:
		test `cat $i | grep -v "^#" |head -n 1`
		if ($status == 0) then
		set j = `cat $i | grep -v "^#" |head -n 1`
			eval set $j
			setenv $NAME
		endif
		breaksw
	endsw
end

set nonomatch
foreach i ( /etc/profile.d/*.csh )
	test -f $i
	if ($status == 0) then
		source $i
	endif
end
unset nonomatch
