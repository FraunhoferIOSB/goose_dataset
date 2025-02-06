# GOOSE Dataset :duck: Repository for the FieldRobotics Workshop Challenge at ICRA 2025

<!-- ![logo](static/goose_logo_share.jpg) -->
![logo](static/goose_logo.png)

<div align="center">

[![Static Badge](https://img.shields.io/badge/GOOSE-PDF?label=arXiv&color=red&link=https%3A%2F%2Farxiv.org%2Fabs%2F2310.16788)](https://arxiv.org/abs/2310.16788)
[![Static Badge](https://img.shields.io/badge/GOOSE_EX-PDF?label=PDF&color=green&link=https%3A%2F%2Fgoose-dataset.de%2Fimages%2FgooseEx.pdf)](https://goose-dataset.de/images/gooseEx.pdf)
[![Static Badge](https://img.shields.io/badge/GOOSE_Website-Web?label=Website&color=blue&link=https%3A%2F%2Fgoose-dataset.de%2F)](https://goose-dataset.de/)
[![Static Badge](https://img.shields.io/badge/Documentation-Web?label=Docs&color=blue&link=https%3A%2F%2Fgoose-dataset.de%2Fdocs%2F)](https://goose-dataset.de/docs/)

</div>

This branch contains the scripts and tools to work with the GOOSE Dataset and run baseline experiments for the Field Robotics workshop challenge at ICRA 2025.

## Download

The data structure and more in-depth information about the format can be found int the [documentation](https://goose-dataset.de/docs/dataset-structure/). The data is divided into 3 splits: train, test and validation. Labeled data is available for train and validation splits. 

It can be downloaded from [our webpage](https://goose-dataset.de/docs/setup/#download-dataset). 

In `scripts` you can find some scripts to directly download and unpack the 2D data.

## Data Visualization

Under `tools`, some scritps can be found to visualize the GOOSE data.

### 2D Data

Run the `tools/visualize_2d_data.py` script to display some images from the downloaded data. Please refer to the script's argument parser for more information.


### 3D Data 

We use the a slightly adapted version of the [semantic-kitti-api](https://github.com/PRBonn/semantic-kitti-api) visualizer, that can be run from the `pointcloud_processing/tools/visualize_3d_data.py`. The only dependency is `python3-vispy`.

The visualizer can be invoked using:
```
python3 visualize_3d_data.py --dataset data/goose/3d/
```

If you want to visualize data from a specific sequence or platform, you can use a regex:

```
python3 visualize_3d_data.py --dataset data/goose/3d/ -r ".*spot_scenario04.*"
```

## Utilities

Under the folder `common` some general configuration files and utils such as color maps can be found.

For more specific tools regarding training and data handling, have a look at the `image_processing` and `pointcloud_processing` subfolders.

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
- [Peter Mortimer](mailto:peter.mortimer@unibw.de)

GOOSE is a project of [Fraunhofer IOSB](https://www.iosb.fraunhofer.de/de/kompetenzen/systemtechnik/mess-regelungs-diagnosesysteme.html), [UniBW Munich](https://www.unibw.de/tas) and [University of Koblenz](https://www.uni-koblenz.de/de/informatik/icv/paulus).
