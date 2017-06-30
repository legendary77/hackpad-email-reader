#!/usr/bin/env bash

# Get full path to the directory of this file
pushd `dirname $0` > /dev/null
SCRIPTPATH=`pwd -P`
popd > /dev/null

VENV_NAME="venv"

LOGO="
====================================
=====   HackPad Email Parser   =====
====================================
"

# Print some intro
echo "$LOGO"

echo "Bootstraping HACKPAD EMAIL PARSER Environment..."

# Update pip
pip install --upgrade pip

# Install virtualenv
pip install virtualenv

# Go into the app root directory
cd "$SCRIPTPATH/../"

# Create venv
[[ -d "$VENV_NAME" ]] || virtualenv -p python3 $VENV_NAME


# Activate Virtual Env
source "$VENV_NAME/bin/activate"

# Upgrade pip
pip install --upgrade pip

# Install Prerequisites
pip install -q -r requirements.txt

deactivate