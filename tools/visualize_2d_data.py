"""
Tool to visualize some frames of the GOOSE(-EX) 2D Dataset
"""

from goosetools import GOOSE_Dataset

import argparse as ap
from typing import List, Optional
from random import randint
from matplotlib import pyplot as plt
from PIL import Image
import numpy as np


def parse_args() -> ap.Namespace:
    parser = ap.ArgumentParser("GOOSE 2D Visualizer")

    parser.add_argument("img_path", type=str, help="Path to images' folder")
    parser.add_argument("lbl_path", type=str, help="Path to labels' folder")

    parser.add_argument(
        "--n_elements",
        type=int,
        default=5,
        help="Number of frames to display. If a list of indices is given, this is ignored. Otherwise n_elements random frames are selected",
    )

    parser.add_argument(
        "--indices",
        nargs="+",
        default=None,
        help="List of indices of the dataset to be displayed",
    )

    parser.add_argument(
        "--overlay",
        action="store_true",
        help="Show an overlay of the semantic map instead of the color map",
    )

    return parser.parse_args()


def overlay_images(A: Image, B: Image, alpha=0.65) -> Image:
    array1 = np.array(A)
    array2 = np.array(B)

    # Define the alpha value for transparency (0-1 where 0 is fully transparent)
    alpha = 0.5  # Adjust this value for transparency

    # Overlay the images using alpha blending
    overlayed_array = (alpha * array1 + (1 - alpha) * array2).astype(np.uint8)

    # Convert back to a PIL image
    return Image.fromarray(overlayed_array)


def show_images(
    dataset: GOOSE_Dataset,
    n_elements: Optional[int] = 5,
    indices: Optional[List[int]] = None,
    overlay: bool = False,
):
    if indices is None:
        assert n_elements is not None
        indices = [randint(0, len(dataset)) for _ in range(n_elements)]

    n_elements = len(indices)

    fig, axs = plt.subplots(n_elements, 3)

    for id, index in enumerate(indices):
        img, sem, inst, color = dataset.get_images(index)

        if overlay:
            color = overlay_images(img, color)

        axs[id, 0].imshow(img)
        axs[id, 1].imshow(color)
        axs[id, 2].imshow(inst)
        axs[id, 0].axis("off")
        axs[id, 1].axis("off")
        axs[id, 2].axis("off")

    axs[0, 0].set_title("RGB Image")
    axs[0, 1].set_title("Semantic Map")
    axs[0, 2].set_title("Instance Map")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    opts = parse_args()

    dataset = GOOSE_Dataset.from_paths(
        opts.img_path, opts.lbl_path, crop=False, resize_size=None, with_instances=True
    )
    show_images(
        dataset, n_elements=opts.n_elements, indices=opts.indices, overlay=opts.overlay
    )
