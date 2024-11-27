"""
This scripts implements a simple training set-up with SuperGradients.

Modify this script to add new functionality or modify the default configuration.

"""

import argparse as ap
import os

import super_gradients as sg
import torch
from super_gradients.common.object_names import Models
from super_gradients.training.metrics.segmentation_metrics import IoU
from torch.utils.data import DataLoader

from super_gradients.training.losses.dice_loss import GeneralizedDiceLoss

from goosetools import GOOSE_Dataset

#######################################
#######################################


def parse_args() -> ap.Namespace:
    parser = ap.ArgumentParser("GOOSE 2D Trainer")

    parser.add_argument("data_path", type=str, help="Path to goose folder")
    parser.add_argument("--epochs", "-e", type=int, default=20)
    parser.add_argument("--batch_size", "-bs", type=int, default=5)
    parser.add_argument("--resize_width", "-rw", type=int, default=768)
    parser.add_argument("--resize_height", "-rh", type=int, default=768)

    parser.add_argument("--lr", "-lr", type=float, default=0.005)

    return parser.parse_args()

#######################################
#######################################


def collate_fn(batch):
    """
    Collate function for the Pytorch Dataloader. If a specific structure is needed for your
    model, change it here.
    """
    imgs, sem_lbls = zip(*batch)

    return torch.stack(imgs), torch.stack(sem_lbls)


#######################################
#######################################

if __name__ == "__main__":
    ## Load the data
    #
    opts = parse_args()

    train_dataset, val_dataset = GOOSE_Dataset.splits_from_path(
        opts.data_path, resize_size=[opts.resize_width, opts.resize_height], crop=True
    )

    ## Set-up for training
    #

    # Create output directory
    EXPERIMENT_NAME = "GOOSE_train"
    WS_PATH = os.getcwd()
    CHECKPOINT_DIR = os.path.join(WS_PATH, "output", "ckpts")

    if not os.path.isdir(CHECKPOINT_DIR):
        os.makedirs(CHECKPOINT_DIR)

    # Params
    BATCH_SIZE = opts.batch_size
    N_EPOCHS = opts.epochs

    # Dataloaders
    train_dataloader = DataLoader(
        train_dataset,
        batch_size=BATCH_SIZE,
        shuffle=True,
        num_workers=5,
        drop_last=True,
        collate_fn=collate_fn,
    )
    val_dataloader = DataLoader(
        val_dataset,
        batch_size=BATCH_SIZE,
        shuffle=True,
        num_workers=5,
        drop_last=True,
        collate_fn=collate_fn,
    )

    # Trainer Set-up
    device = "cuda" if torch.cuda.is_available() else "cpu"
    sg.setup_device(device=device)
    trainer = sg.Trainer(experiment_name=EXPERIMENT_NAME, ckpt_root_dir=CHECKPOINT_DIR)

    ## Load Model
    #
    model = sg.training.models.get(
        model_name=Models.DDRNET_39, num_classes=64, pretrained_weights="cityscapes"
    )
    model.eval()

    # Set-up Training params
    lr_updates = [int(0.3 * N_EPOCHS), int(0.6 * N_EPOCHS), int(0.9 * N_EPOCHS)]
    train_params = {
        "max_epochs": N_EPOCHS,
        "lr_mode": "step",
        "lr_updates": lr_updates,
        "lr_decay_factor": 0.1,
        "initial_lr": opts.lr,
        "optimizer": "sgd",
        "loss": GeneralizedDiceLoss(),
        "average_best_models": False,
        "greater_metric_to_watch_is_better": True,
        "loss_logging_items_names": ["loss"],
        "drop_last": True,
    }

    train_params["train_metrics_list"] = [IoU(num_classes=64)]
    train_params["valid_metrics_list"] = [IoU(num_classes=64)]
    train_params["metric_to_watch"] = "IoU"

    ## Train
    #
    trainer.train(
        model=model,
        training_params=train_params,
        train_loader=train_dataloader,
        valid_loader=val_dataloader,
    )
