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

test -d /etc/env.d
if ($status == 0) then
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
			if ( -r $i ) then
				set body = `cat $i | grep -v "^#"`
				if $status then
					foreach j ( $body )
						eval set $j
						setenv $NAME
					end
				endif
			endif
			breaksw
		endsw
	end
endif

test -d /etc/profile.d
if ($status == 0) then
	set nonomatch
	foreach i ( /etc/profile.d/*.csh )
		test -f $i
		if ($status == 0) then
			source $i
		endif
	end
	unset nonomatch
endif
