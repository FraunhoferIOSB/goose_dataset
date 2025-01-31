# Pointcept

The baseline for pointcloud segmentation is obtained using the [Pointcept](https://github.com/Pointcept/Pointcept) framework with the [PTv3](https://github.com/Pointcept/PointTransformerV3) backbone for semantic segmentation.

Our [fork](https://github.com/FraunhoferIOSB/Pointcept) contains the configurations required to train PTv3 on the GOOSE-Dataset. A docker container is provided for easy use (tested with CUDA_VERSION=11.7 and CUDNN_VERSION=8):

```
git clone -b goose https://github.com/FraunhoferIOSB/Pointcept
cd Pointcept/scripts
./build_image.sh
```

For a development setup, we map our Pointcept repo as well as the dataset into the container. Please adapt both paths in the `scripts/run_image.sh` script to your need.

## Download Pretrained weights

The baseline-weights can be downloaded from the [website](https://goose-dataset.de/models/challenge_ptv3.pth) into the experiment folder:

```
mkdir -p exp/goose/semseg-ptv3-challenge-goose-baseline/model
wget -O exp/goose/semseg-ptv3-challenge-goose-baseline/model/model_best.pth https://goose-dataset.de/models/challenge_ptv3.pth
```

## Testing on GOOSE

You can run the configuration against the val or test splits and generate the submission files for uploading to CodaBench:

```
sh Pointcept/scripts/test.sh -g 1 -d goose -c semseg-pt-v3m1-0-base -n semseg-ptv3-challenge-goose-baseline
```

After successful evaluation on the test split, the resulting `.label` files will be generated in `exp/goose/semseg-ptv3-challenge-goose-baseline/result/submit/`

## Training on GOOSE

To train on the current baseline configuration, you can run:

```
sh ./scripts/train.sh -g 1 -d goose -c semseg-pt-v3m1-0-base -n my-experiment-name
```

## Submitting your results to CodaBench

TODO







