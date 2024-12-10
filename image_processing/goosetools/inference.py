from torchvision.transforms import ToPILImage
import torch


def run_inference(
    img, model, verbose=False, return_img=False, threshold=0.5
) -> torch.Tensor:
    # Run inference
    if len(img.shape) != 4:
        img = torch.unsqueeze(img, 0)
    mask = model(img)
    masks = torch.sigmoid(mask).squeeze()
    if len(masks.shape) < 3:
        masks = torch.stack([1 - masks, masks], dim=0)
    label = torch.max(masks, 0)[1]

    if verbose:
        print(mask.shape)
        print(masks.shape)
        print(label.shape)
        print(torch.unique(label))

    if return_img:
        return ToPILImage()(label.float())
    else:
        return label
