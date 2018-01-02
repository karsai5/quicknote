from setuptools import setup, find_packages

long_description = """
A cursors full screen command line application based on the OSX note taking app
Notational Velocity.
"""

classifiers = [
    # How mature is this project? Common values are
    #   3 - Alpha
    #   4 - Beta
    #   5 - Production/Stable
    'Development Status :: 4 - Beta',

    # Indicate who your project is intended for
    'Intended Audience :: Developers',
    'Topic :: Software Development',

    # Pick your license as you wish (should match "license" above)
     'License :: OSI Approved :: MIT License',

    # Specify the Python versions you support here. In particular, ensure
    # that you indicate whether you support Python 2, Python 3 or both.
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.2',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
]

setup(
    name='quicknote',
    version='1.0.2',
    description='a quick note taking application',
    long_description=long_description,
    scripts=['qn'],
    author='Linus Karsai',
    author_email='karsai5@gmail.com',
    url='https://github.com/karsai5/quicknote',
    license='MIT',
    classifiers=classifiers,
    keywords='notes note development quicknote',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
)
