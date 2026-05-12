Get-ItemProperty `
'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts' |

Export-Csv `
word_real_fonts.csv `
-NoTypeInformation `
-Encoding UTF8