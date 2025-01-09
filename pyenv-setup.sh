#!/bin/sh

pyenv install 3.11.0 
pyenv virtualenv 3.11.0 aie-challenge-3.11.0
pyenv local aie-challenge-3.11.0

python3 -m pip install --upgrade pip
pip install -r requirements.txt
