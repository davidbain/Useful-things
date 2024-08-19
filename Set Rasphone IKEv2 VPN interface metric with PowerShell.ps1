# Sets the persistent interface metric for ALL VPN profiles within Rasphone.pbk, per device. 
# Logic: if metric is currently set to 'automatic' / 0, then change it to a metric of 1. Change the numbers in replace to adjust this. 
# Must be run as a local admin / System. 
((Get-Content -path "C:\ProgramData\Microsoft\Network\Connections\Pbk\rasphone.pbk") -replace 'IpInterfaceMetric=0','IpInterfaceMetric=1') | Set-Content -path "C:\ProgramData\Microsoft\Network\Connections\Pbk\rasphone.pbk"
