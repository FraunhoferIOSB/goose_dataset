from torchvision.transforms import ToPILImage, ToTensor
from PIL import Image
import torch
from typing import Union


def load_image_tensor(img: Union[torch.Tensor, Image.Image, str]):
    if isinstance(img, torch.Tensor):
        return img
    if isinstance(img, str):
        img = Image.open(img).convert("RGB")
    if isinstance(img, Image.Image):
        return ToTensor()(img)
    raise TypeError


def run_inference(
    input_tensor: torch.Tensor,
    model,
    verbose=False,
    threshold=0.5,
) -> torch.Tensor:
    # Run inference
    if len(input_tensor.shape) != 4:
        input_tensor = torch.unsqueeze(input_tensor, 0)
    mask = model(input_tensor)
    masks = torch.sigmoid(mask).squeeze()
    if len(masks.shape) < 3:
        masks = torch.stack([1 - masks, masks], dim=0)
    label = torch.max(masks, 0)[1]

    if verbose:
        print(mask.shape)
        print(masks.shape)
        print(label.shape)
        print(torch.unique(label))

    return label
