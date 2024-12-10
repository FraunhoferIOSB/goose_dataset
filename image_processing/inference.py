import argparse
import fnmatch
import os
from tqdm import tqdm
import super_gradients as sg
from goosetools.inference import load_image_tensor, run_inference
from super_gradients.common.object_names import Models
from PIL import Image
from torchvision.transforms import Resize, InterpolationMode, ToPILImage
import torch
import numpy as np
import matplotlib.pyplot as plt


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument("path", type=str, help="Path to images")
    parser.add_argument("ckpt", type=str, help="Path to checkpoint to load")
    parser.add_argument(
        "--output", "-o", type=str, default="output/inference", help="Path for output"
    )

    ## Pre-processing
    parser.add_argument("--resize", action="store_true")
    parser.add_argument(
        "--input_width",
        "-rw",
        type=int,
        default=768,
        help="Width to resize the image to before inferring",
    )
    parser.add_argument(
        "--input_height",
        "-rh",
        type=int,
        default=768,
        help="Height to resize the image to before inferring",
    )

    opt = parser.parse_args()

    return opt


def find_images(input_path):
    image_paths = []
    image_extensions = ("*.jpg", "*.jpeg", "*.png")

    for dirpath, _, filenames in os.walk(input_path):
        for filename in filenames:
            # Check if the file matches any of the image patterns
            if any(fnmatch.fnmatch(filename, ext) for ext in image_extensions):
                full_path = os.path.join(dirpath, filename)
                relative_path = os.path.relpath(full_path, input_path)
                image_paths.append(relative_path)

    return image_paths


def save_mask_tensor(tensor: torch.Tensor, path: str):
    class_ids_np = tensor.numpy()
    pil_image = Image.fromarray(class_ids_np)
    pil_image.save(path)


if __name__ == "__main__":
    opt = parse_args()
    imgs = find_images(opt.path)

    ckpt: str = opt.ckpt
    ckpt = ckpt.removeprefix("file://")
    model = sg.training.models.get(
        model_name=Models.DDRNET_39,
        num_classes=64,
        pretrained_weights="cityscapes",
        checkpoint_path=ckpt,
    )
    model.eval()

    resize_transform = Resize([opt.input_height, opt.input_width])

    pbar = tqdm(imgs)
    for i in pbar:
        pbar.set_description(i)
        img_tensor = load_image_tensor(os.path.join(opt.path, i))
        orig_size = [img_tensor.shape[2], img_tensor.shape[1]]
        if opt.resize:
            img_tensor = resize_transform(img_tensor)
        res = run_inference(img_tensor, model).numpy()
        result = Image.fromarray(res.astype(np.uint8)).convert("L")
        if opt.resize:
            result = result.resize(orig_size, Image.Resampling.NEAREST)

        output_path = os.path.join(opt.output, i)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        result.save(output_path)
