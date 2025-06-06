import csv
import glob
import os
from typing import Dict, Iterable, List, Optional, Tuple

import numpy as np
import torch
import tqdm
from PIL import Image
from torch.utils.data import Dataset
from torchvision import transforms


def __check_labels(img_path: str, lbl_path: str) -> Tuple[bool, Optional[List]]:
    """
    Check if pair of labels and images exist. Filter non-existing pairs.
    """
    name = os.path.basename(img_path)
    name = (
        name.removesuffix("_windshield_vis.png")
        .removesuffix("_front.png")
        .removesuffix("_camera_left.png")
        .removesuffix("_realsense.png")
    )

    names = []
    for l in ["color", "instanceids", "labelids"]:
        # Check if label exists
        lbl_name = name + "_" + l + ".png"
        if not os.path.exists(os.path.join(lbl_path, lbl_name)):
            names.append(None)
            continue
        names.append(lbl_name)

    return names


def process_goose_folder(img_path: str, lbl_path: str) -> List[Dict]:
    """
    Create a data Dictionary with image paths
    """
    subfolders = glob.glob(os.path.join(img_path, "*/"), recursive=False)
    subfolders = [f.split("/")[-2] for f in subfolders]

    valid_imgs = []
    valid_lbls = []
    valid_insta = []
    valid_color = []

    datadict = []

    for s in tqdm.tqdm(subfolders):
        imgs_p = os.path.join(img_path, s)
        lbls_p = os.path.join(lbl_path, s)
        imgs = glob.glob(os.path.join(imgs_p, "*.png"))
        for i in imgs:
            lbl_names = __check_labels(i, lbls_p)
            if not lbl_names[2]:
                print("No label found for", i)
                continue

            valid_imgs.append(i)
            if lbl_names[0]:
                valid_color.append(os.path.join(lbls_p, lbl_names[0]))
            else:
                valid_color.append(None)
            if lbl_names[1]:
                valid_insta.append(os.path.join(lbls_p, lbl_names[1]))
            else:
                valid_insta.append(None)

            valid_lbls.append(os.path.join(lbls_p, lbl_names[2]))

    for i, m, p, c in zip(valid_imgs, valid_lbls, valid_insta, valid_color):
        datadict.append(
            {
                "img_path": i,
                "semantic_path": m,
                "instance_path": p,
                "color_path": c,
            }
        )

    return datadict


def load_mapping_csv(mapping_csv_path: str = "goose_label_mapping.csv"):
    mapping = []
    with open(mapping_csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for r in reader:
            mapping.append(r)


def load_splits(
    src_path: str, splits: List[str] = ["train", "val"]
) -> Tuple[List[Dict]]:
    """
    Parameters:

        src_path            :   path to dataset

    Returns:

        datadicts           : List of dicts with the dataset information
    """

    img_path = os.path.join(src_path, "images")
    lbl_path = os.path.join(src_path, "labels")

    datadicts = []
    for c in splits:
        print("### " + c.capitalize() + " Data ###")
        datadicts.append(
            process_goose_folder(os.path.join(img_path, c), os.path.join(lbl_path, c))
        )

    return datadicts


class GOOSE_Dataset(Dataset):
    """
    Example Pytorch Dataset Module for GOOSE.
    """

    def __init__(
        self,
        dataset_dict: List[Dict],
        crop: bool = True,
        resize_size: Optional[Iterable[int]] = None,
        crop_ratio: Optional[float] = None,
        with_instances: bool = False,
    ):
        """
        Parameters:
            dataset_dict  [Iter]    : List of  Dicts with the images information generated by *goose_create_dataDict*
            crop          [Bool]    : Whether to make a square crop of the images or not
            resize_size   [Iter]    : List with the target resize size of the images (After the crop if crop == True) (width, height)
            crop_ratio    [Float]   : Ratio for the center crop. If set to None, it is calculated fromt he resize_size
        """
        self.dataset_dict = dataset_dict
        self.transforms = transforms.Compose(
            [
                transforms.ToTensor(),
            ]
        )
        self.resize_size = resize_size
        self.crop = crop

        if crop_ratio is None and resize_size is None and crop:
            print("Both resize_size and crop_ratio are undefined!")
            exit(1)
        
        self.crop_ratio = None
        if crop:
            self.crop_ratio = (
                crop_ratio if crop_ratio is not None else resize_size[0] / resize_size[1]
            )
        
        self.with_instances = with_instances

    def preprocess(self, image):
        """
        Performs a central crop and rescaling of the image

        Parameters:
            image   [PIL.Image]   :   Image to preprocess
        """
        if image is None:
            return None

        if self.crop:
            # Crop in the center
            ir: float = image.width / image.height
            wr: float = self.crop_ratio

            if ir > wr:
                nh = image.height
                nw = int(nh * wr)
            elif wr > ir:
                nw = image.width
                nh = nw // wr
            else:
                nw = image.width
                nh = image.height

            image = transforms.CenterCrop((nh, nw)).forward(image)

        if self.resize_size is not None:
            # Resize to given size
            image = image.resize(self.resize_size, resample=Image.NEAREST)

        return image

    def __getitem__(self, i):
        """
        Parameter:
            i   [int]                   : Index of the image to get

        Returns:
            image_tensor [torch.Tensor] : 3 x H x W Tensor
            label_tensor [torch.Tensor] : H x W Tensor as semantic map
        """
        image = Image.open(self.dataset_dict[i]["img_path"]).convert("RGB")
        label = Image.open(self.dataset_dict[i]["semantic_path"]).convert("L")

        image = self.preprocess(image)
        label = self.preprocess(label)

        image_tensor = self.transforms(image)
        label_tensor = torch.from_numpy(np.array(label)).long()

        if self.with_instances:
            instances = Image.open(self.dataset_dict[i]["instance_path"]).convert("L")
            instances = self.preprocess(instances)

            instances_tensor = torch.from_numpy(np.array(instances)).long()

            return image_tensor, label_tensor, instances_tensor

        return image_tensor, label_tensor

    def __len__(self):
        return len(self.dataset_dict)

    @staticmethod
    def splits_from_path(src_path: str, **kwargs):
        """
        Create a goose Dataset directly from path
        """
        datadict = load_splits(src_path, splits=["train", "val"])

        return (
            GOOSE_Dataset(datadict[0], **kwargs),  # train
            GOOSE_Dataset(datadict[1], **kwargs),  # val
        )

    @staticmethod
    def from_paths(img_path: str, lbl_path: str, **kwargs):
        datadict = process_goose_folder(img_path, lbl_path)

        return GOOSE_Dataset(datadict, **kwargs)

    def get_images(self, index):
        image = Image.open(self.dataset_dict[index]["img_path"]).convert("RGB")
        label = Image.open(self.dataset_dict[index]["semantic_path"]).convert("L")
        
        color = None
        instances = None
        if(self.dataset_dict[index]["color_path"]):
            color = Image.open(self.dataset_dict[index]["color_path"]).convert("RGB")
        if(self.dataset_dict[index]["instance_path"]):
            instances = Image.open(self.dataset_dict[index]["instance_path"]).convert("L")

        return image, label, instances, color
    
    def get_original_label(self, index, as_tensor=False):
        label = Image.open(self.dataset_dict[index]["semantic_path"]).convert("L")
        if as_tensor:
            label = torch.from_numpy(np.array(label)).long()
        return label


if __name__ == "__main__":
    splits = GOOSE_Dataset.splits_from_path("/home/miguel/datasets/goose/goose2d")
    for s in splits:
        print(f"Loaded GOOSE dataset with {len(s)} items.")
