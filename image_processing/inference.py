import argparse
import fnmatch
import os

import numpy as np
import super_gradients as sg
from goosetools.inference import load_image_tensor, run_inference
from PIL import Image
from super_gradients.common.object_names import Models
from torchvision.transforms import Resize
from tqdm import tqdm

from goosetools.utils import str2bool, overlay_masks, get_colormap


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
    
    ## Output
    parser.add_argument(
        "--overlay",
        type=str2bool,
        default=True
    )
    parser.add_argument(
        "--cmap_path",
        type=str,
        default=None,
        help="Path to color map json of type -> {id : [r,g,b]}"
    )
    
    ## Data
    parser.add_argument("--n_classes", "-nc", type=int, default=64)

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


if __name__ == "__main__":
    opt = parse_args()
    imgs = find_images(opt.path)
    n_classes = opt.n_classes

    ckpt: str = opt.ckpt
    ckpt = ckpt.removeprefix("file://")
    model = sg.training.models.get(
        model_name=Models.PP_LITE_B_SEG75,
        num_classes=n_classes,
        pretrained_weights="cityscapes",
        checkpoint_path=ckpt,
    )
    model.eval()

    resize_transform = Resize([opt.input_height, opt.input_width])
    
    cmap_dict = get_colormap(opt.cmap_path, n_classes)

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
        
        if opt.overlay:
            overlay = overlay_masks(np.transpose(img_tensor.numpy(), (1, 2, 0)), np.array(result), color_map=cmap_dict, alfa=0.7) * 255
            overlay_img = Image.fromarray(overlay.astype(np.uint8)).convert("RGB")
            output_path = os.path.join(opt.output, "overlay",i)
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            overlay_img.save(output_path)
