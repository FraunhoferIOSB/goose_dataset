# GOOSE Dataset: Image Processing

Quickly load GOOSE Data in your own projects with the `goosetools` package.

```python
from goosetools import GOOSE_Dataset
# Directly load our data as a Pytorch Dataset in one line
train_dataset, val_datset = GOOSE_Dataset.splits_from_path("/home/miguel/datasets/goose/goose2d")
```

## Set-up

<details>
  
<summary><b>General requirements (Tested)</b></summary>

- Python 3.9.
- torch = 1.13.1
  - <https://pytorch.org/get-started/locally/>
- The python packages specified in `config/requirements.txt`
- SuperGradients is only needed for the examples.

</details>

<br>

<details>
<summary><b>Conda automatic Set-up</b></summary>

We recomend using a [conda environment](https://docs.anaconda.com/miniconda/miniconda-install/):

```bash
source setup.sh
```

This will install and activate a conda environment with the necessary dependencies.

</details>

## Visualization

Run the `visualize_2d_data.py` script to display some images from the downloaded data. Please refer to the script's argument parser for more information.

## ICRA 25 - Workshop

The baseline checkpoint can be downloaded [here](https://bwsyncandshare.kit.edu/s/MNN2Y9SRtDQXAxq/download/challenge_ppliteseg.pth). It uses the Supergradients' PPLiteSeg _PP_LITE_B_SEG75_ model.


The model was trained with a fixed resolution of 768 x 512 pixels (for all GOOSE & GOOSE-EX training Data) using some contrast and brightness data augmentations.

To check the baseline model against the validation split:

```bash
python evaluation.py /path/to/goose/ /path/to/ckpt -rh 512 --iou true -nc 9 --test_split_name val
```

With the baseline you should expect these values when evaluating against the GOOSE validation split:

```
Metric:
	-> 0: 0.9269827604293823
	-> 1: 0.7645474672317505
	-> 2: 0.9482942819595337
	-> 3: 0.8249742388725281
	-> 4: 0.6437028050422668
	-> 5: 0.8964053988456726
	-> 6: 0.8717983961105347
	-> 7: 0.527831494808197
	-> 8: 0.9510554671287537
Mean: 0.8172880411148071
Filetered Mean: 0.8172880411148071
```

To infer on images with the baseline:

```bash
python inference.py /path/to/goose /path/to/ckpt -rh 512 --resize -nc 9
```


### Data Submission

To submit your data to the [Codabench]() competition, generate ID masks for all the images in the test set and pack them in a zip file. It should have the same folder structure as the test images:

```
-- submission.zip
    |
    |--- scene01
    |     |-- <imagename1>_labelids.png
    |     |-- <imagename2>_labelids.png
    |
    |--- scene02
          |-- ...
```

**Make sure that the labels have the same name format as in the actual dataset**. They have to end in `_labelids.png`. If you have files with the same name as the input RGB images, you can use the script in `tools/rename.bash` to generate the labels with the correct name format.

## Examples: Training, Evaluation & Inference

The following tools are based on [SuperGradients](https://github.com/Deci-AI/super-gradients) and mere usage examples on how to use and itegrate GOOSE in your own projects, or on how to use the checkpoints provided in our [webpage](https://goose-dataset.de/docs/setup/#2d-image-segmentation).
The focus is not to implement a new training framework, therefore these are also simplified versions of the scripts used to train the models and achieve the results presented in our papers.

If you are just looking for a data loader for GOOSE, just install the goosetools package with `pip install -e .` and you are good to go (make sure you have the necessary dependencies)!

### 2D Semantic Training

Use the script `semantic_train.py` to train a semantic segmentation model.
For that we use the framework [SuperGradients](https://github.com/Deci-AI/super-gradients).
There are multiple models available within this framework and the training tool enables a very simple
yet rich training process.

**Example usage of `semantic_train.py`**
```bash
python semantic_train.py /path/to/goose --epochs 20 --batch_size 10 -rw 1024 -rh 768 -lr 0.005 --crop
```

SuperGradients automatically logs some paramters to TensorBoard. It can be seen with:

```bash
tensorboard --logdir=output
```

### 2D Semantic Evaluation

To evaluate the performance of a trained checkpoint the script `evaluation.py` can be used.

**Example usage of `evaluation.py`**
```bash
python evaluation.py /path/to/goose /path/to/ckpt -rw 1024 -rh 768 --crop --iou true --vis_res false
```

The results will be printed to the console and saved as a file to the output directory (default = output/evaluation/\<timestamp>)

### Model inference

To run the images through the models and save the inferred results use the `inference.py` script.

**Example usage of `inference.py`**
```bash
python inference.py /path/to/goose /path/to/ckpt -rw 1024 -rh 768 --resize --overlay true
```

The results will be saved to the output directory (default = output/inference/)
