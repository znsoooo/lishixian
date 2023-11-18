:: Build two packages at once time.

@echo off
for /f %%i in (VERSION.txt) do (set ver=%%i)
echo Version: %ver%
echo.

rename lsx lishixian
python setup.py sdist
echo.
pip install dist/lishixian-%ver%.tar.gz
echo.

rename lishixian lsx
python setup.py sdist
echo.
pip install dist/lsx-%ver%.tar.gz
echo.

rename lsx lishixian
pause
