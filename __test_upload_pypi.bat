:: Update current version to pypi.org

@echo off
set python=py -3.6

for /f "tokens=2 delims='" %%i in (lishixian/version.py) do (set ver=%%i)
echo Version: %ver%

%python% -m twine upload dist/lsx-%ver%.tar.gz
%python% -m twine upload dist/lishixian-%ver%.tar.gz

pause
