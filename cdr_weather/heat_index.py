import numpy as np

def kelvin_to_celsius(t: np.ndarray) -> np.ndarray:
    """_summary_

    Args:
        t (np.ndarray): temperature in degrees Kelvin

    Returns:
        np.ndarray: temperature in degrees Celsius
    """
    return t - 273.15

def kelvin_to_fahrenheit(t: np.ndarray) -> np.ndarray:
    """_summary_

    Args:
        t (np.ndarray): temperature in degrees Kelvin

    Returns:
        np.ndarray: temperature in degrees Fahrenheit
    """
    return (t - 273.15) * (9 / 5) + 32


def compute_heat_index(t: np.ndarray, rh: np.ndarray) -> np.ndarray:
    """_summary_

    Args:
        t (float): temperature in degrees Fahrenheit
        rh (float): relative humidity in percent

    Returns:
        float: heat index
    """
    heat_index = np.zeros(t.shape)
    below_80f = t < 80
    t_below_80f = t[below_80f]
    rh_below_80f = rh[below_80f]

    t_above_80f = t[~below_80f]
    rh_above_80f = rh[~below_80f]

    # compute for t < 80
    heat_index[below_80f] = 0.5 * (
        t_below_80f + 61.0 + ((t_below_80f - 68.0) * 1.2) + (rh_below_80f * 0.094)
    )

    # compute for t >= 80
    tsq = t_above_80f**2
    rhsq = rh_above_80f**2
    heat_index[~below_80f] = (
        -42.379
        + (2.04901523 * t_above_80f)
        + (10.14333127 * rh_above_80f)
        - (0.22475541 * t_above_80f * rh_above_80f)
        - (0.00683783 * tsq)
        - (0.05481717 * rhsq)
        + (0.00122874 * tsq * rh_above_80f)
        + (0.00085282 * t_above_80f * rhsq)
        - (0.00000199 * tsq * rhsq)
    )
    return heat_index


def compute_heat_index_with_adjustments(
    t: np.ndarray, rh: np.ndarray, masked=True
) -> np.ndarray:
    """_summary_

    Args:
        t (np.ndarray): temperature in degrees Fahrenheit
        rh (np.ndarray): relative humidity in percent

    Returns:
        np.ndarray: adjusted heat index
    """
    heat_index = compute_heat_index(t, rh)
    if masked:
        mask = t.mask
        assert np.all(mask == rh.mask)
    # adjustment 1
    condition1 = (t >= 80) & (t <= 112) & (rh < 13)
    rh_cond1 = rh[condition1]
    t_cond1 = t[condition1]
    heat_idx_adj1 = (13 - rh_cond1) / 4 * np.sqrt((17 - abs(t_cond1 - 95)) / 17)
    heat_index[condition1] = heat_index[condition1] - heat_idx_adj1

    # adjustment 2
    condition2 = (t >= 80) & (t <= 87) & (rh > 85)
    rh_cond2 = rh[condition2]
    t_cond2 = t[condition2]
    heat_idx_adj2 = ((rh_cond2 - 85) / 10) * ((87 - t_cond2) / 5)
    heat_index[condition2] = heat_index[condition2] + heat_idx_adj2
    if masked:
        heat_index = np.ma.masked_array(heat_index, mask=mask)
    return heat_index
