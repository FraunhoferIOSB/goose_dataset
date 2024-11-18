#!/bin/bash
echo "**************************************"
echo "Configuring Virtual Environment"
echo "**************************************"

conda env create -f config/env.yaml

conda activate goosenv

echo "**************************************"
echo "Installation finished!!"
echo "**************************************"
