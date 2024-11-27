# GOOSE Dataset :duck: Official Repository

<!-- ![logo](static/goose_logo_share.jpg) -->
![logo](static/goose_logo.png)

This repository contains some tools for training and benchmarking with the GOOSE Dataset.

- Visit the official GOOSE website for more information: [goose-dataset.de](https://goose-dataset.de/).

- Our first publication: [The GOOSE Dataset for Perception in Unstructured Environments](https://arxiv.org/abs/2310.16788).

- Our second paper (in review): [Excavating in the Wild: The GOOSE-Ex Dataset for Semantic Segmentation](https://goose-dataset.de/images/gooseEx.pdf).

## Set-up

### Environment

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

### Data

The data structure and more in-depth information about the format can be found int the [documentation](https://goose-dataset.de/docs/dataset-structure/). The data is divided into 3 splits: train, test and validation. Labeled data is available for train and validation splits. 

It can be downloaded from [our webpage](https://goose-dataset.de/docs/setup/#download-dataset). 

In `scripts` you can find some scripts to directly download and unpack the data.

## Data Visualization

Under `tools`, some scritps can be found to visualize the GOOSE data.

### 2D Data

Run the `tools/visualize_2d_data.py` script to display some images from the downloaded data. Please refer to the script's argument parser for more information.


### 3D Data [TODO]


## Training & Evaluation [TODO]

### 2D Semantic Training

Use the script `tools/semantic_train.py` to train a semantic segmentation model.
For that we use the framework [SuperGradients](https://github.com/Deci-AI/super-gradients).
There are multiple models available within this framework and the training tool enables a very simple
yet rich training process.

**Example usage of `tools/semantic_train.py`**
```bash
python tools/semantic_train.py /path/to/goose --epochs 20 --batch_size 10 -rw 1024 -rh 768 -lr 0.005
```

SuperGradients automatically logs some paramters to TensorBoard. It can be seen with:

```bash
tensorboard --logdir=output
```

## Other tools

## Acknowledgements [TODO]

## Citation

Please cite us if this data is useful for you work:

```bibtex
@article{goose-dataset,
    author = {Peter Mortimer and Raphael Hagmanns and Miguel Granero
              and Thorsten Luettel and Janko Petereit and Hans-Joachim Wuensche},
    title = {The GOOSE Dataset for Perception in Unstructured Environments},
    url={https://arxiv.org/abs/2310.16788},
    conference={2024 IEEE International Conference on Robotics and Automation (ICRA)}
    year = 2024
}

@article{goose-ex-dataset,
    author = {Raphael Hagmanns and Peter Mortimer and Miguel Granero
              and Thorsten Luettel and Janko Petereit},
    title = {Excavating in the Wild: The GOOSE-Ex Dataset for Semantic Segmentation},
    url={},
    conference={TBA}
    year = 2024
} 
```

## License

- This **repository** is licensed under the **MIT License**.
- The **data** is published under the **CC BY-SA 4.0 License**.

## Mantainers

- [Miguel Granero](mailto:miguel.granero@iosb.fraunhofer.de)
- [Raphael Hagmanns](mailto:raphael.hagmanns@iosb.fraunhofer.de)
