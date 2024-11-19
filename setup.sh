#!/bin/bash
echo "**************************************"
echo "Configuring Virtual Environment"
echo "**************************************"

conda env create -f config/env.yaml

conda activate goosenv

pip install -e .

echo "**************************************"
echo "Installation finished!!"
echo "**************************************"
