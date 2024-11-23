import os
import sys
import shutil
import setuptools

# fix to import module in current directory (cwd not include in sys.path in embedded python)
sys.path.insert(0, os.getcwd())

# setup packages names
pkg_name = setuptools.find_packages()[0]
pkgs = [pkg_name, pkg_name + '.docs', pkg_name + '.scripts']

# clean up last run
shutil.rmtree(pkg_name + '/docs', ignore_errors=True)
shutil.rmtree(pkg_name + '/scripts', ignore_errors=True)

# prepare files
os.makedirs(pkg_name + '/docs')
shutil.copy('README.md', pkg_name + '/docs/README.md')
shutil.copy('LICENSE.txt', pkg_name + '/docs/LICENSE.txt')
shutil.copytree('scripts', pkg_name + '/scripts')

setuptools.setup(
    name=pkg_name,
    version=__import__(pkg_name).__version__,
    author='Shixian Li (znsoooo)',
    author_email='lsx7@sina.com',
    description='Lite Software eXtension',
    long_description=open('README.md', encoding='u8').read(),
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
    packages=pkgs,

    # install_requires=['pkg_name'],
    # extras_requires={'pkg_name': ['pkg_name']},
    license='MIT License',
    entry_points={'console_scripts': ['{0}={0}.__main__:run'.format(pkg_name)]},
    package_data={'': ['*.*']},
    keywords='lishixian lsx',
)

# clean up
shutil.rmtree(pkg_name + '/docs', ignore_errors=True)
shutil.rmtree(pkg_name + '/scripts', ignore_errors=True)
