#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='bvatar',
    version='1.0.a3',
    url='https://github.com/smileychris/bvatar',
    #download_url='',
    description='Random-art avatar generation',
    license='BSD',
    long_description=open('README.rst').read(),
    author='Chris Beaven',
    author_email='smileychris@gmail.com',
    platforms=['any'],
    scripts=['bvatar.py'],
    entry_points={
        'console_scripts': [
            'bvatar = bvatar:main',
        ],
    },
    install_requires=['six', 'docopt', 'bitarray'],
    extras_require = {
        'bitmap': ['pillow'],
    },
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Multimedia :: Graphics',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
