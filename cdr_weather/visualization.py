import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
from typing import Tuple


def make_heatmap(
    extent: list,
    data: np.ndarray,
    title: str = "Raster Data Heatmap",
    origin: str = "upper",
    cmap: str = "turbo",
    vmin: float = -30,
    vmax: float = 100,
    flip: bool = False,
) -> Tuple[mpl.figure.Figure, mpl.axes.Axes]:
    """
    Creates a heatmap of the raster data.
    input:
        extent: list of the extent of the raster data
        data: numpy array of the raster data
        title: title of the plot
        origin: origin of the plot
        cmap: colormap to use
        vmin: minimum value of the colormap
        vmax: maximum value of the colormap
        flip: whether to flip the data or not
    output:
        fig: matplotlib figure
        ax: matplotlib axis
    """
    if flip:
        np.flipud(data)
    # Create a figure and axis for the plot
    fig, ax = plt.subplots(figsize=(10, 10))

    cmap = eval("mpl.cm." + cmap)
    cmap.set_bad("white", 0.3)
    # Plot the raster data as a heatmap
    heatmap = ax.imshow(
        data, extent=extent, origin=origin, cmap=cmap, vmin=vmin, vmax=vmax
    )

    # Add a colorbar to the heatmap
    fig.colorbar(heatmap, ax=ax, shrink=0.5, aspect=5)

    # Set title and labels if needed
    ax.set_title(title)
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    return fig, ax
