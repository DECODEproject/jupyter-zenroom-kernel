from setuptools import setup, find_packages

try:
    import pypandoc
    description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
    description = ''

setup(
    name='jupyter_zenroom_kernel',
    version='0.0.1',
    description='Jupyter kernel for Zenroom. Small, secure and portable virtual machine for crypto language processing',
    long_description=description,
    author='Dyne development team',
    author_email='puria@dyne.org',
    url='https://github.com/puria/jupyter-zenroom-kernel',
    license='AGPLv3+',
    keywords='',
    platforms='Linux, Mac OS X, Windows',
    install_requires=[
        'metakernel==0.20.14',
        'notebook>=5.4.1',
    ],
    packages=find_packages(include=['zenroom', 'zenroom.*']),
    package_data={},
    classifiers=[
        'Framework :: Jupyter',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Programming Language :: Python :: 3',
        'Programming Language :: Zenroom',
        'Topic :: Security :: Cryptography',
        'Topic :: System :: Distributed Computing',
    ]
)
