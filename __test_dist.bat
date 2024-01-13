:: Build two packages at once time.

@echo off
set python=py -3.6

for /f "tokens=2 delims='" %%i in (lishixian/version.py) do (set ver=%%i)
echo Version: %ver%
echo.

rename lsx lishixian
%python% setup.py sdist
echo.
%python% -m pip install dist/lishixian-%ver%.tar.gz
echo.

rename lishixian lsx
%python% setup.py sdist
echo.
%python% -m pip install dist/lsx-%ver%.tar.gz
echo.

rename lsx lishixian
pause
