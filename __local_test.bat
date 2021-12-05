:: Build two packages at once time.

for /f %%a in (VERSION.txt) do (set ver=%%a)
echo %ver%

ren lsx lishixian
python setup.py sdist
pip install dist/lishixian-%ver%.tar.gz

ren lishixian lsx
python setup.py sdist
pip install dist/lsx-%ver%.tar.gz

ren lsx lishixian
pause
