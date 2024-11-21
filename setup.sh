#!/bin/sh

# Check if virtualenv is installed; if not, install it
if ! pip show virtualenv > /dev/null 2>&1; then
    echo "virtualenv is not installed. Installing..."
    pip install virtualenv
fi

# Create a virtual environment named 'venv'
virtualenv -p python3.9 venv

# Activate the virtual environment
. venv/bin/activate

# Install dependencies from requirements.txt
pip install -r requirements.txt

echo "Setup complete. Virtual environment 'venv' is activated."
