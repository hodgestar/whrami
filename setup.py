import os
from setuptools import setup, find_packages


def read_file(filename):
    filepath = os.path.join(os.path.dirname(__file__), filename)
    return open(filepath, 'r').read()

setup(
    name='whrami',
    version='0.1.0',
    url='http://github.com/hodgestar/whrami',
    license='BSD',
    description=(
        'A text-based interactive fiction guessing game.'),
    long_description=read_file('README.md'),
    author='Simon Cross',
    author_email='hodgestar@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'aiohttp',
        'click',
    ],
    entry_points='''
    [console_scripts]
    whrami = whrami.cli:main
    ''',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet :: WWW/HTTP',
    ],
    zip_safe=False
)
