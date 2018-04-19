from setuptools import setup, find_packages

test_deps = [
    'coverage',
    'nose',
    'jupyter_kernel_test',
]

setup(
    name='jupyter_zenroom_kernel',
    version='0.0.6',
    description='Jupyter kernel for Zenroom. Small, secure and portable virtual machine for crypto language processing',
    author='Dyne Development Team',
    author_email='puria@dyne.org',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    project_urls={
        'Tracker': 'https://github.com/puria/jupyter-zenroom-kernel/issues',
        'Zenroom project': 'https://zenroom.dyne.org/',
        'Decode Project': 'https://decodeproject.eu/',
    },
    url='https://github.com/puria/jupyter-zenroom-kernel',
    license='AGPLv3+',
    keywords='',
    platforms='Linux, Mac OS X, Windows',
    python_requires='>=3',
    install_requires=[
        'metakernel==0.20.14',
        'notebook>=5.4.1',
        'html2text',
    ],
    tests_require=test_deps,
    extras_require={'test': test_deps},
    packages=find_packages(include=['zenroom', 'zenroom.*']),
    package_data={'zenroom': 'binaries/*'},
    classifiers=[
        'Framework :: Jupyter',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Programming Language :: Python :: 3',
        'Topic :: Security :: Cryptography',
        'Topic :: System :: Distributed Computing',
    ]
)
