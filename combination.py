import matplotlib.pyplot as plt
from option_pricing import *
import numba


# FNX BTC: 1, ETH: 1.15, BNB=3.0
sigma = 1.15
r = 0.05
expiration = 1. / 365 * 0
borrow = 'B'


@numba.vectorize("float64(float64, float64)", nopython=True, cache=True)
# @numba.jit("float64[:](float64, float64[:])", nopython=True)
def lp_pnl(L, x):
    if borrow == 'B':
        return L * np.sqrt(x) - L * x + x - 1
    elif borrow == 'U':
        return L * (np.sqrt(x) - 1)
    elif borrow == 'B+U':
        if L == 2.5:
            return 5/6 * (L * np.sqrt(x) - L * x + x - 1) + 1/6 * L * (np.sqrt(x) - 1)
        elif L == 3:
            return 0.75 * (L * np.sqrt(x) - L * x + x - 1) + 0.25 * L * (np.sqrt(x) - 1)
        else:
            print("Leverage unavailable.")
            return 0.
    else:
        print("Specify debt type.")
        return 0.


# 先vectorize再call jit用时2.0s，jit[:]再call jit[:]用时1.7s
@numba.vectorize("float64(float64, float64, float64, float64, float64)", nopython=True, cache=True)
# @numba.jit("float64[:](float64[:], float64, float64, float64, float64)", nopython=True, cache=True)
def option_pnl(x, call_strike, put_strike, call_size, put_size):
    call = vanilla_option(x, call_strike,  expiration, r, sigma, 1)
    put = vanilla_option(x, put_strike,  expiration, r, sigma, 2)
    return call_size * call + put_size * put


@numba.jit("float64(float64, float64, float64, float64)", nopython=True, cache=True)
def APR(L, maximum_loss, duration, premium):
    if borrow == 'B':
        return (0.516 * L + (0.17 - 0.108) * (L - 1) + maximum_loss / duration) / (1 + premium)
    elif borrow == 'U':
        return (0.516 * L + (0.058 - 0.2) * (L - 1) + maximum_loss / duration) / (1 + premium)
    elif borrow == 'B+U':
        if L == 2.5:
            return (5/6 * (0.516 * L + (0.17 - 0.108) * (L - 1) + maximum_loss / duration)
                    + 1/6 * (0.516 * L + (0.058 - 0.2) * (L - 1) + maximum_loss / duration)) / (1 + premium)
        elif L == 3:
            return (0.75 * (0.516 * L + (0.17 - 0.108) * (L - 1) + maximum_loss / duration)
                    + 0.25 * (0.516 * L + (0.058 - 0.2) * (L - 1) + maximum_loss / duration)) / (1 + premium)
        else:
            print("Leverage unavailable.")
            return 0.
    else:
        return 0.0


@numba.jit("float64[:](float64)", nopython=True, cache=True)
def price_range(L):
    if L > 1:
        LTVi = (L-1) / L
        if borrow == 'B':
            LTVf = 0.8
            liquidation = (LTVf / LTVi) ** 2
            x = np.arange(0.5, liquidation + 0.01, 0.01)
        elif borrow == 'U':
            LTVf = 0.8
            liquidation = (LTVi / LTVf) ** 2
            x = np.arange(liquidation, 2, 0.01)
        elif borrow == 'B+U':
            LTVf = 0.8
            liquidation = (LTVf / LTVi) ** 2
            x = np.arange(1. / liquidation, liquidation + 0.01, 0.01)
        else:
            print("Specify debt type.")
            x = np.arange(0.5, 2, 0.01)
    else:
        x = np.arange(0.5, 2.5, 0.01)
    return x


def plot_combo(L, call_strike, call_size, put_strike, put_size, length=30, exercise_cost=1.0, premium_premium=1.0):
    x = price_range(L)
    duration = 1. / 365 * length

    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.figure(figsize=(16, 8))
    call_premium = vanilla_option1(1, call_strike, duration, r, sigma, option=1)
    put_premium = vanilla_option1(1, put_strike, duration, r, sigma, option=2)
    premium = (call_size * call_premium + put_size * put_premium) * premium_premium
    option = exercise_cost * option_pnl(x, call_strike, put_strike, call_size, put_size) - premium
    lp = lp_pnl(L, x)
    maximum_loss = np.min(lp + option)
    apr = APR(L, maximum_loss, duration, premium)
    plt.xlabel("相对价格", fontsize=12)
    plt.ylabel("相对盈亏", fontsize=12)
    plt.title("收益曲线", fontsize=12)
    plt.plot(x, lp, label='{}倍杠杆LP'.format(L))
    plt.plot(x, option,
             label='时长{:d}天，{:.2f}个Call行权价{:.2f}，{:.2f}个Put行权价{:.2f}\n Call单价{:.3f}，Put单价{:.3f}，IV {:.1%}'
             .format(length, call_size, call_strike, put_size, put_strike, call_premium, put_premium, sigma))
    plt.plot(x, lp + option,
             label='组合收益，最大回撤:{:.2%}，权利金:{:.3f}，预测APR:{:.2%}'.format(maximum_loss, premium, apr))
    plt.legend(loc="best", prop={'size': 12})
    plt.grid(linestyle='--')
    plt.show()
