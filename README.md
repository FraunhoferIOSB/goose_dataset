# GOOSE Dataset :duck: Official Repository

<!-- ![logo](static/goose_logo_share.jpg) -->
![logo](static/goose_logo.png)

This repository contains some tools for training and benchmarking with the GOOSE Dataset.

- Visit the official GOOSE website for more information: [goose-dataset.de](https://goose-dataset.de/).

- Our first publication: [The GOOSE Dataset for Perception in Unstructured Environments](https://arxiv.org/abs/2310.16788).

- Our second paper (in review): [Excavating in the Wild: The GOOSE-Ex Dataset for Semantic Segmentation](https://goose-dataset.de/images/gooseEx.pdf).

## Set-up [TODO]

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

**Example 2D set-up with GOOSE-EX**
```bash
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
```

## Data Visualization [TODO]

## Training & Evaluation [TODO]

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

## Mantainers

- [Miguel Granero](mailto:miguel.granero@iosb.fraunhofer.de)
- [Raphael Hagmanns](mailto:raphael.hagmanns@iosb.fraunhofer.de)
