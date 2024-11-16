@ reg delete HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\FileExts\.py /f
@ taskkill /f /im explorer.exe & start explorer & start explorer "%cd%"
@ pause
