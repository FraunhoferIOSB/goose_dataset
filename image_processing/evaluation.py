import argparse
import json
import os
from datetime import datetime

import super_gradients as sg
import torch
import tqdm
from goosetools import GOOSE_Dataset
from goosetools.data import load_splits
from goosetools.inference import run_inference
from goosetools.utils import str2bool
from matplotlib import pyplot as plt
from super_gradients.common.object_names import Models
from torchmetrics import JaccardIndex
import numpy as np
from torchvision import transforms
from torchvision.transforms import InterpolationMode


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument("path", type=str, help="Path to images")
    parser.add_argument("ckpt", type=str, help="Path to checkpoint to load")
    parser.add_argument(
        "--output", "-o", type=str, default="output", help="Path for output"
    )

    ## Pre-processing
    parser.add_argument("--crop", action="store_true")
    parser.add_argument(
        "--use_original_label",
        action="store_true",
        help="Whether to evaluate with the original labels. That means, resize the output of the model to the original size",
    )
    parser.add_argument("--resize_width", "-rw", type=int, default=768)
    parser.add_argument("--resize_height", "-rh", type=int, default=768)

    ## Results
    parser.add_argument(
        "--iou",
        type=str2bool,
        default=True,
        help="Whether to calculate the mean IoU or not. [Default True]",
    )
    parser.add_argument(
        "--vis_res",
        type=str2bool,
        default=False,
        help="Whether to visualize the results or not. [Default False]",
    )

    ## Data
    parser.add_argument("--n_classes", "-nc", type=int, default=64)

    opt = parser.parse_args()

    return opt


def write_results(result: torch.Tensor, path: str, config: dict):
    with open(os.path.join(path, "config.json"), "w") as f:
        json.dump(config, f)

    class_results = [f"{i}: {x.item()}" for i, x in enumerate(result)]
    results_txt = [
        "Metric:\n\t-> " + "\n\t-> ".join(class_results),
        f"Mean: {result.mean()}",
        f"Filetered Mean: {result[torch.nonzero(result)].mean()}",
    ]
    with open(os.path.join(path, "results.txt"), "w") as f:
        for line in results_txt:
            f.write(line + "\n")
            print(line)


def visualize(img: torch.Tensor, gt: torch.Tensor, res: torch.Tensor):
    _, axes = plt.subplots(1, 3, figsize=(15, 5))

    axes[0].imshow(img.permute(1, 2, 0).numpy())
    axes[0].axis("off")
    axes[0].set_title("RGB Image")

    axes[1].imshow(gt.numpy())
    axes[1].axis("off")
    axes[1].set_title("Ground Truth")

    axes[2].imshow(res.numpy())
    axes[2].axis("off")
    axes[2].set_title("Inferred")

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    opt = parse_args()

    n_classes = opt.n_classes
    calculate_iou = opt.iou
    visualize_res = opt.vis_res

    now = datetime.now()

    ## Load model
    ckpt: str = opt.ckpt
    ckpt = ckpt.removeprefix("file://")
    model = sg.training.models.get(
        model_name=Models.PP_LITE_B_SEG75,
        num_classes=n_classes,
        pretrained_weights="cityscapes",
        checkpoint_path=ckpt,
    )
    model.eval()

    ## Load data
    validation_dict = load_splits(opt.path, ["test"])[0]
    validation_dataset = GOOSE_Dataset(
        validation_dict,
        crop=opt.crop,
        resize_size=[opt.resize_width, opt.resize_height],
        with_instances=False,
    )

    metric = JaccardIndex(n_classes, multilabel=False, reduction="none")
    metric.reset()
    try:
        print("*** Processing images ***")
        print("*************************")
        pbar = tqdm.tqdm(range(len(validation_dataset)))
        for i in pbar:
            img, sem_map = validation_dataset[i]

            mask = run_inference(img, model=model, threshold=0.5)
            
            if opt.use_original_label:
                sem_map = validation_dataset.get_original_label(i, True)
                resize = transforms.Resize([sem_map.shape[0], sem_map.shape[1]], interpolation=InterpolationMode.NEAREST)
                mask = resize(mask.unsqueeze(0)).squeeze(0)
                               
            if visualize_res:
                visualize(img, sem_map, mask)

            if calculate_iou:
                metric.update(mask, sem_map)
                pbar.set_description(f"Mean: {metric.compute().mean()}")

    except KeyboardInterrupt:
        print("Interrupted by user, saving results until now.")
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)

    output_path = os.path.join(
        opt.output, "evaluation", now.strftime("%m-%d-%Y_%H:%M:%S")
    )
    os.makedirs(output_path, exist_ok=False)

    if calculate_iou:
        result = metric.compute()
        write_results(result, output_path, vars(opt))
