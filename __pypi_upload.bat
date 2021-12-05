:: Update current version to pypi.org

for /f %%a in (VERSION.txt) do (set ver=%%a)
echo %ver%

python -m twine upload dist/lsx-%ver%.tar.gz
python -m twine upload dist/lishixian-%ver%.tar.gz

pause
