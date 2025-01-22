# Find all of the available providers and channels in Microsoft Windows,
# this command will generate a list for both
# Got this info on: https://adamtheautomator.com/get-winevent/#Listing_Event_Log_Providers
Get-WinEvent -ListProvider * | Format-Table -Autosize

# Get all the events?
Get-WinEvent -FilterHashTable @{'LogName' = 'Application'; 'StartTime' = (Get-Date -Hour 0 -Minute 0 -Second 0)} | Select-Object TimeCreated, ID, ProviderName, LevelDisplayName, Message | Format-Table -AutoSize



# This seems to be the correct way to get this done
===========
$Channel = @('Microsoft-Windows-Security-Auditing','Microsoft-Windows-Sysmon')
Foreach ($Sub in $Channel) {
	$MainCollector = Get-WinEvent -ListProvider $Sub
	$MainCollector.Events | ConvertTo-Json -Depth 5 > $Sub.json	
}

$MainCollector = Get-WinEvent -ListProvider $Channel
$MainCollector.Events | ConvertTo-Json -Depth 5 > windows-sysmon.json

==========


# The following commands get the events and metadata description
# from the DHCP Server Channel, this can be easily changed to 
# other channels as needed
$Channel = "Microsoft-Windows-Security-Auditing"
$SubChannel = @('Application','Security','Setup','System','Forwarded Events')
$FullProvider = Get-WinEvent -ListProvider $Channel
Foreach ($Sub in $SubChannel) {
	$Path = $Channel+"-"+$Sub
	$FullProvider.Events | Where-Object {$_.LogLink.LogName -eq $Path} > $Path.txt
}