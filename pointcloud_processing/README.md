# Pointcept

The baseline for pointcloud segmentation is obtained using the [Pointcept](https://github.com/Pointcept/Pointcept) framework with the [PTv3](https://github.com/Pointcept/PointTransformerV3) backbone for semantic segmentation.

Our [fork](https://github.com/FraunhoferIOSB/Pointcept) contains the configurations required to train PTv3 on the GOOSE-Dataset. A docker container is provided for easy use (tested with CUDA_VERSION=11.7 and CUDNN_VERSION=8):

```
git clone -b goose https://github.com/FraunhoferIOSB/Pointcept
cd Pointcept/scripts
./build_image.sh
```

For a development setup, we overlay our Pointcept repo as well as the dataset into the container. Please adapt both paths in the `scripts/run_image.sh` script to your need.

## Download Pretrained weights

The baseline-weights can be downloaded from the [website](https://goose-dataset.de/models/challenge_ptv3.pth) into the experiment folder:

```
cd /workspace/Pointcept
mkdir -p exp/goose/semseg-ptv3-challenge-goose-baseline/model
wget -O exp/goose/semseg-ptv3-challenge-goose-baseline/model/model_best.pth https://goose-dataset.de/models/challenge_ptv3.pth
```

## Testing on GOOSE

You can run the configuration against the val or test splits and generate the submission files for uploading to CodaBench:

```
sh ./scripts/test.sh -g 1 -d goose -c semseg-pt-v3m1-0-base -n semseg-ptv3-challenge-goose-baseline
```

After successful evaluation on the test split, the resulting `.label` files will be generated in `exp/goose/semseg-ptv3-challenge-goose-baseline/result/submit/`

## Training on GOOSE

To train on the current baseline configuration, you can run:

```
sh ./scripts/train.sh -g 1 -d goose -c semseg-pt-v3m1-0-base -n my-experiment-name
```

The baseline model evaluated on the validation set should perform like that: 

```
Val result: mIoU/mAcc/allAcc 0.8096/0.8576/0.9197
Class_0 - other Result: iou/accuracy 0.9686/0.9766
Class_1 - artificial_structures Result: iou/accuracy 0.8773/0.9065
Class_2 - artificial_ground Result: iou/accuracy 0.7097/0.7871
Class_3 - natural_ground Result: iou/accuracy 0.8220/0.9487
Class_4 - obstacle Result: iou/accuracy 0.4554/0.5121
Class_5 - vehicle Result: iou/accuracy 0.8954/0.9197
Class_6 - vegetation Result: iou/accuracy 0.9179/0.9509
Class_7 - human Result: iou/accuracy 0.8302/0.8589
```


## Submitting your results to CodaBench

TODO
- zip results
- upload







