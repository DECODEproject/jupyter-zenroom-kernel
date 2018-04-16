<p align="center"><a href="https://decodeproject.eu" target="_blank" rel="noopener noreferrer"><img width="200" src="https://decodeproject.eu/sites/all/themes/marmelo_base/img/logo.svg" alt="Decode logo"></a></p>
<p align="center"><a href="https://dyne.org" target="_blank" rel="noopener noreferrer"><img width="200" src="https://secrets.dyne.org/static/img/swbydyne.png" alt="Software by Dyne"></a></p>

#Jupyter zenroom kernel 

A [Zenroom](http://zenroom.dyne.org) :key: Jupyter [kernel](http://jupyter.readthedocs.io/en/latest/projects/kernels.html) that uses [metakernel](https://github.com/Calysto/metakernel)

## Dependencies
* Jupyter Notebook
* Python 3
* Zenroom

## Install

Before installing you probably want to create a [**virtual environment**](https://virtualenv.pypa.io/en/stable/) as per python best practices.
Once you activate your virtualenv you can install the kernel with the following commands:

    $ pip install jupyter_zenroom_kernel
    $ python3 -m zenroom install --user

If the zenroom binary (shared or static) is installed system wide and/or is in your $PATH, then you just run jupyter as you would normally do

    $ jupyter notebook

If the binary is not in your path you have to set an environment variable **ZENROOM_BIN** with the absolute path of the binary 

## What is zenroom?
Zenroom is a brand new, small and portable virtual machine for cryptographic operations and is part of the [DECODE project](https://decodeproject.eu) about data-ownership and [technological sovereignty](https://www.youtube.com/watch?v=RvBRbwBm_nQ).
You can read more about it on [https://zenroom.dyne.org/]()

## todo
 - [ ] zenroom_exec_buf
 - [x] foldable json rendering
 - [x] cell syntax highlighting
 - [x] mark lines on syntax errors
 - [ ] unit testing
 - [ ] better documentation