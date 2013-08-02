on run argv
	
	set asanaBin to "./asana.sh"
	set argc to count argv
	if argc is greater than 0 then
		set asanaDate to "by " & item 1 of argv
	else
		set asanaDate to "by today"
	end if
	
	tell application "Google Chrome" to set _URL to URL of active tab of front window
	tell application "Google Chrome" to set _TITLE to title of active tab of front window
	
	set asanaStatus to do shell script "'" & asanaBin & "' '" & _TITLE & "' '" & _URL & "' " & asanaDate
	
	return asanaStatus
	
end run