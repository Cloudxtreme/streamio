#!/bin/bash

requirements="fabric"

if [[ "$VIRTUAL_ENV" == "" ]]; then
    # Just in case pyth0n2.7 was installed with --prefix=/usr/local
    PATH="/usr/local/bin/:$PATH"

    curl -o - https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py | python2.7 -
    curl -o - https://raw.github.com/pypa/pip/master/contrib/get-pip.py | python2.7 -
fi

pip install -U $requirements

echo "DONE!"
echo "Please run: fab build"
echo "For help, Type: fab help"
