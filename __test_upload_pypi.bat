:: Update current version to pypi.org

@echo off
set python=py -3.6

for /f %%a in (VERSION.txt) do (set ver=%%a)
echo Version: %ver%

%python% -m twine upload dist/lsx-%ver%.tar.gz
%python% -m twine upload dist/lishixian-%ver%.tar.gz

pause
