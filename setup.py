import os
import shutil
import setuptools

keys = ['readme', 'license', 'todo', 'version']
os.makedirs('lishixian/docs', exist_ok=True)
for file in os.listdir():
    if any(file.lower().startswith(k) for k in keys):
        shutil.copy(file, 'lishixian/docs/' + file.lower())

with open('VERSION.txt') as f:
    version = f.read().strip()

with open('README.md', encoding='u8') as f:
    long_description = f.read()

setuptools.setup(
    name='lishixian',
    version=version,
    author='Lishixian(znsoooo)',
    author_email='lsx7@sina.com',
    description='lishixian package',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/znsoooo/lishixian',
    project_urls={
        'Bug Tracker': 'https://github.com/znsoooo/lishixian/issues',
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Framework :: IDLE',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
    ],
    packages=setuptools.find_packages(),

    # install_requires=['windnd'], # for drag-open file feature
    # extras_requires={'windnd': ['windnd']},
    license='MIT License',
    package_data={'': ['*.*']},
    keywords='lishixian lsx',
)
