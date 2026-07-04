@echo off
for %%i in ("%cd%") do git bundle create "%%~nxi%1.git" --all %1
pause
