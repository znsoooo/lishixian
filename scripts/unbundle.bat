@echo off
if not "%~1" == "" (
    set "name=%~1"
) else (
    for %%i in (*.git) do set name=%%~nxi
)
git init
git fetch "%name%"
git checkout FETCH_HEAD
git fetch "%name%" *:*
pause
