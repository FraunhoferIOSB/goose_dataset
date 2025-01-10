# GOOSE Dataset: Image Processing

## Set-up

<details>
  
<summary><b>General requirements (Tested)</b></summary>

- Python 3.9.
- torch = 1.13.1
  - <https://pytorch.org/get-started/locally/>
- The python packages specified in `config/requirements.txt`

</details>

<br>

<details>
<summary><b>Conda Set-up</b></summary>

We recomend using a [conda environment](https://docs.anaconda.com/miniconda/miniconda-install/):

```bash
source setup.sh
```

This will install and activate a conda environment with the necessary dependencies.

</details>

## Training & Evaluation [TODO]

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
python evaluation.py /path/to/goose /path/o/ckpt -rw 1024 -rh 768 --crop --iou true --vis_res false
```

The results will be printed to the console and saved as a file to the output directory (default = output/evaluation/\<timestamp>)

### Model inference

To run the images through the models and save the inferred results use the `inference.py` script.

**Example usage of `inference.py`**
```bash
python inference.py /path/to/goose /path/o/ckpt -rw 1024 -rh 768 --resize --overlay true --vis_res false
```

The results will be saved to the output directory (default = output/inference/)