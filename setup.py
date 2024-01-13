import shutil
import setuptools

pkg = setuptools.find_packages()
pkg_name = pkg[0]

shutil.copy('README.md', pkg_name + '/docs/README.md')
shutil.copy('LICENSE.txt', pkg_name + '/docs/LICENSE.txt')

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
    packages=pkg,

    # install_requires=['pkg_name'],
    # extras_requires={'pkg_name': ['pkg_name']},
    license='MIT License',
    entry_points={'console_scripts': ['{0}={0}.__main__:run'.format(pkg_name)]},
    package_data={'': ['*.*']},
    keywords='lishixian lsx',
)
