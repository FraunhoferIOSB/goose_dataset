import argparse
import json

import super_gradients as sg
import torch
import tqdm
from goosetools import GOOSE_Dataset
from goosetools.data import load_splits
from goosetools.inference import run_inference
from super_gradients.common.object_names import Models
from torchmetrics import JaccardIndex
from datetime import datetime
import os


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument("path", type=str, help="Path to images")
    parser.add_argument("ckpt", type=str, help="Path to checkpoint to load")
    parser.add_argument(
        "--output", "-o", type=str, default="output", help="Path for output"
    )

    ## Pre-processing
    parser.add_argument("--crop", action="store_true")
    parser.add_argument("--resize_width", "-rw", type=int, default=768)
    parser.add_argument("--resize_height", "-rh", type=int, default=768)

    opt = parser.parse_args()

    return opt


def write_results(result: torch.Tensor, path: str, config: dict):
    with open(os.path.join(path, "config.json"), "w") as f:
        json.dump(config, f)

    class_results = [f"{i}: {x.item()}" for i, x in enumerate(result)]
    results_txt = [
        "Metric:\n\t->" + "\n\t-> ".join(class_results),
        f"Mean: {result.mean()}",
        f"Filetered Mean: {result[torch.nonzero(result)].mean()}",
    ]
    with open(os.path.join(path, "results.txt"), "w") as f:
        for line in results_txt:
            f.write(line + "\n")
            print(line)


if __name__ == "__main__":
    opt = parse_args()

    now = datetime.now()
    output_path = os.path.join(
        opt.output, "inference", now.strftime("%m-%d-%Y_%H:%M:%S")
    )
    os.makedirs(output_path, exist_ok=False)

    ## Load model
    ckpt: str = opt.ckpt
    ckpt = ckpt.removeprefix("file://")
    model = sg.training.models.get(
        model_name=Models.DDRNET_39,
        num_classes=64,
        pretrained_weights="cityscapes",
        checkpoint_path=ckpt,
    )
    model.eval()

    ## Load data
    validation_dict = load_splits(opt.path, ["val"])[0]
    validation_dataset = GOOSE_Dataset(
        validation_dict,
        crop=opt.crop,
        resize_size=[opt.resize_width, opt.resize_height],
    )

    n_classes = 64
    metric = JaccardIndex(n_classes, multilabel=False, reduction="none")
    metric.reset()
    try:
        print("*** Processing images ***")
        print("*************************")
        pbar = tqdm.tqdm(range(len(validation_dataset)))
        for i in pbar:
            img, sem_map = validation_dataset[i]
            mask = run_inference(img, model=model, return_img=False, threshold=0.5)
            metric.update(mask, sem_map)
            pbar.set_description(f"Mean: {metric.compute().mean()}")
    except KeyboardInterrupt:
        print("Interrupted by user, saving results until now.")
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)

    result = metric.compute()
    write_results(result, output_path, vars(opt))
