import numpy as np


# # function to convert meters per second to miles per hour
# mstomph <- function(r) {return(r * 2.23694)}
def meters_per_second_to_mph(vs: np.ndarray) -> np.ndarray:
    """_summary_

    Args:
        vs (np.ndarray): wind speed in meters per second

    Returns:
        np.ndarray: wind speed in miles per hour
    """
    return vs * 2.23694


# windchill_celsius <- function(t, vs) {
#   wc = 13.712 +
#     (0.6215 * t) -
#     (11.37 * (vs^0.16)) +
#     (0.3965 * t * (vs^0.16))
# }
def compute_wind_chill_celsius(t: np.ndarray, vs: np.ndarray) -> np.ndarray:
    """_summary_

    Args:
        t (np.ndarray): temperature in degrees Celsius
        vs (np.ndarray): wind speed in meters per second

    Returns:
        np.ndarray: wind chill temperature in degrees Celsius
    """
    wc = 13.712 + (0.6215 * t) - (11.37 * (vs**0.16)) + (0.3965 * t * (vs**0.16))
    return wc

# wind chill calculation function
# to be used with temperature in degrees F and wind velocity in mph
# windchill <- function(t, vs) {
#   wc = 35.75 +
#     (0.6215 * t) -
#     (35.75 * (vs^0.16)) +
#     (0.4275 * t * (vs^0.16))
# }

def compute_wind_chill_farhenheit(t: np.ndarray, vs: np.ndarray) -> np.ndarray:
    """_summary_

    Args:
        t (np.ndarray): temperature in degrees Fahrenheit
        vs (np.ndarray): wind speed in miles per hour

    Returns:
        np.ndarray: wind chill temperature in degrees Fahrenheit
    """
    wc = 35.75 + (0.6215 * t) - (35.75 * (vs**0.16)) + (0.4275 * t * (vs**0.16))
    return wc