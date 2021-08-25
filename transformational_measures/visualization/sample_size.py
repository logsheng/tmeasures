import numpy as np
import matplotlib.pyplot as plt
from .. import MeasureResult
from pathlib import Path
from typing import List


def relative_error(reference: MeasureResult, x: MeasureResult):
    error = 0
    n = 0
    for reference_layer, layer in zip(reference.layers, x.layers):
        # comparing with e_rel = |(x-y)| / (|x|+|y|)
        # Note that if (|x|-|y|) ~= 0 then (x-y) ~= 0,
        # So we set e_rel = 0 to avoid division by 0
        num = np.abs(reference_layer - layer)
        den =  np.abs(reference_layer)+np.abs(layer)
        error_layer = num/den
        error_layer[np.isclose(den,0.0)]=0
        error += error_layer.sum()
        n += np.prod(layer.shape)
    return error / n


def get_heatmap_values(results: 'np.ndarray[MeasureResult]', reference: MeasureResult):
    # Calcuate the relative error between the reference and each value of the result array
    def compare(r: MeasureResult): return relative_error(reference, r)
    compare_v = np.vectorize(compare)
    return compare_v(results)



def plot_relative_error_heatmap(results: 'np.ndarray[MeasureResult]', reference: MeasureResult, plot_filepath: Path,
                                labels_samples: List[str], labels_transformations: List[str]):
    # plot a heatmap of relative errors between the MeasureResults in `results` and `reference`
    heatmap = get_heatmap_values(results, reference)
    f, ax = plt.subplots()
    im = ax.imshow(heatmap, cmap="hot",vmin=0,vmax=1)
    ax.set_xticklabels(labels_samples)
    ax.set_yticklabels(labels_transformations)
    ax.set_xlabel("Transformations")
    ax.set_ylabel("Samples")
    cbar = ax.figure.colorbar(im, ax=ax)

    for i in range(heatmap.shape[0]):
        for j in range(heatmap.shape[1]):
            value_str = f"{heatmap[i, j]:.3f}"
            text = ax.text(j, i, value_str,
                           ha="center", va="center", color="g")

    plt.savefig(plot_filepath, bbox_inches="tight")
    plt.close()
