@echo off

for /f "tokens=2 delims='" %%i in (lishixian/version.py) do (set ver=%%i)
echo lsx version:
echo   %ver%
echo.

echo python versions:
py -0
echo.

pause
echo.

for /f %%i in ('py -0') do (
    echo ====================
    echo.
    echo pip install on python %%i ...
    echo.
    py %%i -m pip install dist\lsx-%ver%.tar.gz -U
    echo.
    py %%i -c "print('import lsx-%%s on python-%%s' %% (__import__('lsx').__version__, __import__('sys').version.split()[0]))"
    echo.
)
echo ====================
echo.

pause
