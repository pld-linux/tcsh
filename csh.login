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
		grep -v "^#" $i | head -n 1 > /dev/null
		if ($status == 0) then
			set backslash_quote
			set j = `grep -v "^#" $i |head -n 1`
			eval set "$j"
			# FIXME: how to retrieve something like $$NAME ??
			# This is not working
			setenv $NAME "$NAME"
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
