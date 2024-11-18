#!/bin/bash

## Download the data
wget https://goose-dataset.de/storage/gooseEx_2d_train.zip
wget https://goose-dataset.de/storage/gooseEx_2d_val.zip
wget https://goose-dataset.de/storage/gooseEx_2d_test.zip

## Unzip all three zip files
unzip gooseEx_2d_test.zip -d gooseEx_2d_test
unzip gooseEx_2d_train.zip -d gooseEx_2d_train
unzip gooseEx_2d_val.zip -d gooseEx_2d_val

## Create the target directory structure
mkdir -p goose-dataset/images/{test,train,val} goose-dataset/labels/{train,val}

## Move files from each unzipped folder to the final structure
mv gooseEx_2d_test/{CHANGELOG,goose_label_mapping.csv,LICENSE} goose-dataset/
mv gooseEx_2d_test/images/test/* goose-dataset/images/test/
mv gooseEx_2d_train/images/train/* goose-dataset/images/train/
mv gooseEx_2d_train/labels/train/* goose-dataset/labels/train/
mv gooseEx_2d_val/images/val/* goose-dataset/images/val/
mv gooseEx_2d_val/labels/val/* goose-dataset/labels/val/