:: Update current version to pypi.org

@echo off
set python=py -3.6

for /f %%i in (VERSION.txt) do (set ver=%%i)
echo Version: %ver%

%python% -m twine upload dist/lsx-%ver%.tar.gz
%python% -m twine upload dist/lishixian-%ver%.tar.gz

pause
