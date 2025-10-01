#!/bin/bash

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies from requirements.txt
pip install -r requirements.txt

echo "Virtual environment setup complete!"
echo "To activate the virtual environment, run: source venv/bin/activate"
echo "To deactivate, run: deactivate"
