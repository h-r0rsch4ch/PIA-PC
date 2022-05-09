Write-Host "Se esta obteniendo el cache del DNS..."
$dns2 = ipconfig /displaydns

Write-Host "Creando txt con IpConfig/Dns..."
"COMMAND: ifconfig /displaydns `r`n `r`n", $dns2 | Out-File -FilePath "DNS-DisplayDNS.txt"
