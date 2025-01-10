import argparse
import numpy as np
import matplotlib
import json

def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ("yes", "true", "t", "y", "1"):
        return True
    elif v.lower() in ("no", "false", "f", "n", "0"):
        return False
    else:
        raise argparse.ArgumentTypeError("Boolean value expected.")
    
def remapColor(color: list):
    remap = False
    for c in color:
        if c > 1:
            remap = True
            break
    if remap:
        color = [c / 255.0 for c in color]

    return color 
 
    
def get_colormap(path: str = None, n_classes: int = 64) -> dict:
    cmap_dict = {}

    if not path:
        cmap = matplotlib.colormaps["viridis"].resampled(n_classes)
        for i in range(cmap.colors.shape[0]):
            cmap_dict[i] = cmap.colors[i][0:3]
    else:
        print("Opening colormap at:", path)
        with open(path, "r") as f:
            cmap_dict = json.load(f)

        cmap_dict = {int(k): remapColor(v) for k, v in cmap_dict.items()}

    if cmap_dict == {}:
        cmap_dict = {1: (1, 1, 0.4)}

    #cmap = matplotlib.colors.ListedColormap(list(cmap_dict.values()))
    
    return cmap_dict
    
    
def overlay_masks(
    img: np.ndarray, mask: np.ndarray, color_map: dict = {1: (1, 0, 0)}, alfa=0.6
) -> np.ndarray:
    """
    Takes an image and a segmentation map and performs an overly with color 'color_map'

    Parameters:

        - img       : Image H x W x C where C = 1 or 3

        - mask      : Mask H x W

        - color_map : Dict with one color per value in the semantic map.
                        If no entry is found, the value is not used in the overlay

        - alfa      : Transparency

    Returns:

        - overlay   : Resulting overlay H x W x 3
    """
    overlay = img.copy()

    assert len(overlay.shape) == 3
    assert overlay.shape[-1] == 1 or overlay.shape[-1] == 3

    if overlay.shape[-1] == 1:
        overlay = np.concatenate([overlay, overlay, overlay], axis=-1)
    values = np.unique(mask)
    for v in values:
        if v in color_map.keys():
            m = (mask == v).astype(bool)
            masked_color = np.zeros(overlay.shape)
            masked_color[m] = color_map[v]

            overlay[m] = overlay[m] * (1 - alfa)
            overlay = overlay + (masked_color * alfa)
    if img.dtype != np.uint8:
        return overlay
    return overlay.astype(np.uint8)