# GOOSE Dataset :duck: Repository

<!-- ![logo](static/goose_logo_share.jpg) -->
![logo](static/goose_logo.png)

<div align="center">

[![Static Badge](https://img.shields.io/badge/GOOSE-PDF?label=arXiv&color=red&link=https%3A%2F%2Farxiv.org%2Fabs%2F2310.16788)](https://arxiv.org/abs/2310.16788)
[![Static Badge](https://img.shields.io/badge/GOOSE_EX-PDF?label=PDF&color=green&link=https%3A%2F%2Fgoose-dataset.de%2Fimages%2FgooseEx.pdf)](https://goose-dataset.de/images/gooseEx.pdf)
[![Static Badge](https://img.shields.io/badge/GOOSE_Website-Web?label=Website&color=blue&link=https%3A%2F%2Fgoose-dataset.de%2F)](https://goose-dataset.de/)
[![Static Badge](https://img.shields.io/badge/Documentation-Web?label=Docs&color=blue&link=https%3A%2F%2Fgoose-dataset.de%2Fdocs%2F)](https://goose-dataset.de/docs/)

</div>



## :warning: Check out our [ICRA25 Challenge](https://norlab-ulaval.github.io/icra_workshop_field_robotics/#competition)!

<details>

<summary>Field Robotics Workshop Challenge Information</summary>
<br>

This branch currently contains the scripts and tools to work with the GOOSE Dataset and run baseline experiments for the [Field Robotics workshop challenge at ICRA 2025](https://norlab-ulaval.github.io/icra_workshop_field_robotics/#competition).


More information on how to participate can be found in the [Codabench Challenge website]() and the `image_processing` and `pointcloud_processing` subfolders.

### Category Labels for the ICRA25 Challenge

For the challenge, we use the simplified label set listed below. This version of the labels can be downloaded from [here](https://goose-dataset.de/storage/2d_challenge.zip) and used to replace the original ones.

| name                  | label_key | hex     |
|-----------------------|-----------|---------|
| other                 | 0         | #A9A9A9 |
| artificial_structures | 1         | #DE88DE |
| artificial_ground     | 2         | #EBFF3B |
| natural_ground        | 3         | #A1887F |
| obstacle              | 4         | #FFC107 |
| vehicle               | 5         | #F44336 |
| vegetation            | 6         | #4CAF50 |
| human                 | 7         | #8FB0FF |
| sky                   | 8         | #2196F3 |

</details>

## Download

The data structure and more in-depth information about the format can be found int the [documentation](https://goose-dataset.de/docs/dataset-structure/). The data is divided into 3 splits: train, test and validation. Labeled data is available for train and validation splits. 

It can be downloaded from [our webpage](https://goose-dataset.de/docs/setup/#download-dataset). 

In `scripts` you can find some sample scripts to directly download and unpack the 2D data.

## Utilities

Under the folder `common` some general configuration files and utils such as color maps can be found.

For more specific tools regarding training and data handling, have a look at the `image_processing` and `pointcloud_processing` subfolders.

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
