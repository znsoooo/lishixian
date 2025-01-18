@echo off
echo HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\FileExts\.py [DELETE] > repair-idle.ini
regini repair-idle.ini
del repair-idle.ini
taskkill /f /im explorer.exe & start explorer & start explorer "%cd%"
pause
