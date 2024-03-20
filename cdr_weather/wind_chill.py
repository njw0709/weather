import numpy as np

# windchill_celsius <- function(t, vs) {
#   wc = 13.712 +
#     (0.6215 * t) -
#     (11.37 * (vs^0.16)) +
#     (0.3965 * t * (vs^0.16))
# }

def compute_wind_chill(t: np.ndarray, vs: np.ndarray) -> np.ndarray:
    """_summary_

    Args:
        t (np.ndarray): temperature in degrees Fahrenheit
        vs (np.ndarray): wind speed in miles per hour

    Returns:
        np.ndarray: wind chill temperature in degrees Fahrenheit
    """
    wc = 13.712 + (0.6215 * t) - (11.37 * (vs**0.16)) + (0.3965 * t * (vs**0.16))
    return wc