# /etc/cshrc

# System wide rc file for (t)csh

if ($?prompt) then
  [ "$SHELL" = /bin/tcsh ]
  if ($status == 0) then
    set prompt='[%n@%m %c]$ ' 
  else
    set prompt=\[`id -nu`@`hostname -s`\]\$\ 
  endif
endif

test -d /etc/shrc.d
if ($status == 0) then
	set nonomatch
        foreach i ( /etc/shrc.d/*.csh )
		test -f $i
		if ($status == 0) then
               		source $i
		endif
        end
	unset nonomatch
endif
