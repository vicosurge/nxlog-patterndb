# Windows Events taken from Channels mentioned below
# This only gets the schema/structure, it will not get events
# as such from the channels
$Channel = @('Microsoft-Windows-Security-Auditing','Microsoft-Windows-Sysmon')
Foreach ($Sub in $Channel) {
	echo "Writing content of $Sub"
	$MainCollector = Get-WinEvent -ListProvider $Sub
	$MainCollector.Events | ConvertTo-Json -Depth 5 > "$Sub.json"
}