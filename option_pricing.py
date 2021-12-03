import numpy as np
import numba
from math import erfc, sqrt

SQRT2 = sqrt(2.0)


# @numba.jit("float64(float64)", nopython=True)
@numba.vectorize("float64(float64)", nopython=True, cache=True)
def normcdf(x):
    """Normal cumulative distribution function
    """
    # If X ~ N(0,1), returns P(X < x).
    return erfc(-x / SQRT2) / 2.0


# @numba.jit("float64(float64, float64)", nopython=True)
@numba.vectorize("float64(float64, float64)", nopython=True, cache=True)
def clip(x, min):
    """Max between x and min
    """
    if x < min:
        return min
    return x


@numba.vectorize("float64(float64, float64, float64, float64, float64, float64, int16)", nopython=True, cache=True)
# @numba.jit(["float64[:](float64[:], float64, float64, float64, float64, float64, int16)",
#             "float64(float64, float64, float64, float64, float64, float64, int16)"], nopython=True, cache=True)
# @numba.jit("float64(float64, float64, float64, float64, float64, float64, int16)", nopython=True)
# @numba.jit(nopython=True)
def vanilla_option(S, K, T, r, q, sigma, option):
    """Option pricing for array

    :param S: spot price
    :param K: strike price
    :param T: time to maturity in years
    :param r: risk-free interest rate for stablecoin
    :param q: risk-free interest rate for crypto
    :param sigma: standard deviation of log of price of underlying
    :param option: 1=call, 2=put
    """
    if T:
        d1 = (np.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = (np.log(S / K) + (r - q - 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        if option == 1:
            return S * np.exp(-q * T) * normcdf(d1) - K * np.exp(-r * T) * normcdf(d2)
        else:
            return K * np.exp(-r * T) * normcdf(-1. * d2) - S * np.exp(-q * T) * normcdf(-1. * d1)
    else:
        if option == 1:
            return clip(S - K, 0.)
        else:
            return clip(K - S, 0.)


@numba.jit("float64(float64, float64, float64, float64, float64, float64, int16)", nopython=True, cache=True)
# @numba.jit(nopython=True)
def vanilla_option1(S, K, T, r, q, sigma, option=1):
    """Option pricing for float

    :param S: spot price
    :param K: strike price
    :param T: time to maturity in years
    :param r: risk-free interest rate for stablecoin
    :param q: risk-free interest rate for crypto
    :param sigma: standard deviation of log of price of underlying
    :param option: 1=call, 2=put
    """
    if T:
        d1 = (np.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = (np.log(S / K) + (r - q - 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        if option == 1:
            return S * np.exp(-q * T) * normcdf(d1) - K * np.exp(-r * T) * normcdf(d2)
        else:
            return K * np.exp(-r * T) * normcdf(-1. * d2) - S * np.exp(-q * T) * normcdf(-1. * d1)
    else:
        if option == 1:
            return clip(S - K, 0.)
        else:
            return clip(K - S, 0.)
