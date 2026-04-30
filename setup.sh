#!/bin/bash

python -m venv fas-bach
source fas-bach/bin/activate
pip install -r requirements.txt

./scripts/getDataset.sh

jupyter-notebook
