@echo off
set url_base=http://localhost:3000/repos
if not "%~1" == "" (
    set "url=%~1"
) else (
    for %%i in ("%cd%") do set url=%url_base%/%%~ni.git
)
git push --tags "%url%" refs/remotes/origin/*:refs/heads/*
pause
