import os
import shutil
import setuptools

pkg = setuptools.find_packages()

keys = ['readme', 'license', 'todo', 'version']
os.makedirs(pkg[0] + '/docs', exist_ok=True)
for file in os.listdir():
    if any(file.lower().startswith(k) for k in keys):
        shutil.copy(file, pkg[0] + '/docs/' + file.lower())

with open('VERSION.txt') as f:
    version = f.read().strip()

with open('README.md', encoding='u8') as f:
    long_description = f.read()

setuptools.setup(
    name=pkg[0],
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
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
    ],
    packages=pkg,

    # install_requires=['pkg_name'],
    # extras_requires={'pkg_name': ['pkg_name']},
    license='MIT License',
    package_data={'': ['*.*']},
    keywords='lishixian lsx',
)
