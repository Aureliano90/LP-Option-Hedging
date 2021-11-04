import matplotlib.pyplot as plt
from option_pricing import *
import numba

# annualized volatility
sigma = 0.8
# risk-free interest rate
r = 0.05

# debt type
# B for borrowing crypto, U for borrowing stablecoin, B+U for pseudo neutral strategy
borrow = 'B'
# combination.borrow = 'U'
# combination.borrow = 'B+U'

# liquidation debt ratio
LTVf = 0.8

# APR from DEX without leverage including trading fees and liquidity mining rewards
apr_dex = 0.3
# APR from yield aggregators for borrowing crypto
# APR in ALPHA/ALPACA minus borrowing interest
apr_farm_B = 0.1 - 0.1
# APR from yield aggregators for borrowing stablecoin
# APR in ALPHA/ALPACA minus borrowing interest
apr_farm_U = 0.1 - 0.2


@numba.vectorize("float64(float64, float64)", nopython=True, cache=True)
# @numba.jit("float64[:](float64, float64[:])", nopython=True)
def lp_pnl(L, x):
    """PnL of leveraged LP

    :param L: leverage
    :param x: underlying price
    """
    if borrow == 'B':
        return L * np.sqrt(x) - L * x + x - 1
    elif borrow == 'U':
        return L * (np.sqrt(x) - 1)
    elif borrow == 'B+U':
        if L < 2:
            print("Leverage must not be less than 2 for pseudo neutral strategy.")
            return 0.
        else:
            # a is the ratio of initial capital that is used to open a farming position that borrows crypto.
            # 1-a is used to open a farming position that borrows stablecoin.
            # a <= 1
            # delta = 0 = a * (L/2 - L + 1) + (1 - a) * L/2 = -aL + a + L/2
            a = L / 2 / (L - 1)

            return a * (L * np.sqrt(x) - L * x + x - 1) + (1 - a) * L * (np.sqrt(x) - 1)
    else:
        print("Specify debt type.")
        return 0.


# 先vectorize再call jit用时2.0s，jit[:]再call jit[:]用时1.7s
@numba.vectorize("float64(float64, float64, float64, float64, float64, float64)", nopython=True, cache=True)
# @numba.jit("float64[:](float64[:], float64, float64, float64, float64, float64)", nopython=True, cache=True)
def option_pnl(x, exercise: float, call_strike, put_strike, call_size, put_size):
    """Payoff of the option combination

    :param x: underlying price
    :param exercise: days to expiration at exercise / selling
    """
    call = vanilla_option(x, call_strike, exercise / 365, r, sigma, 1)
    put = vanilla_option(x, put_strike, exercise / 365, r, sigma, 2)
    return call_size * call + put_size * put


@numba.jit("float64(float64, float64, float64, float64)", nopython=True, cache=True)
def APR(L, maximum_loss, duration, premium):
    """Minimum effective farming APR after maximum impermanent loss and option premium

    :param L: leverage
    :param maximum_loss: maximum impermanent loss of LP plus options
    :param duration: duration of farming in years
    :param premium: premium paid for buying options
    """
    if borrow == 'B':
        return (apr_dex * L + apr_farm_B * (L - 1) + maximum_loss / duration) / (1 + premium)
    elif borrow == 'U':
        return (apr_dex * L + apr_farm_U * (L - 1) + maximum_loss / duration) / (1 + premium)
    elif borrow == 'B+U':
        if L == 2.5:
            return (5 / 6 * (0.516 * L + (0.17 - 0.108) * (L - 1) + maximum_loss / duration)
                    + 1 / 6 * (0.516 * L + (0.058 - 0.2) * (L - 1) + maximum_loss / duration)) / (1 + premium)
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
    """Price range according to leverage

    :param L: leverage
    """
    if L > 1:
        # initial debt ratio
        LTVi = (L - 1) / L
        if borrow == 'B':
            # price at liquidation
            liquidation = (LTVf / LTVi) ** 2
            x = np.arange(0.5, liquidation + 0.01, 0.01)
        elif borrow == 'U':
            liquidation = (LTVi / LTVf) ** 2
            x = np.arange(liquidation, 2, 0.01)
        elif borrow == 'B+U':
            liquidation = (LTVf / LTVi) ** 2
            x = np.arange(1. / liquidation, liquidation + 0.01, 0.01)
        else:
            print("Specify debt type.")
            x = np.arange(0.5, 2, 0.01)
    else:
        x = np.arange(0.5, 2.5, 0.01)
    return x


def plot_combo(L, call_strike, call_size, put_strike, put_size, dte: float = 30, exercise: float = 0, exercise_cost=1.0,
               premium_premium=1.0):
    """Plot PnL graphs

    :param L: leverage
    :param dte: days to expiration
    :param exercise: days to expiration at exercise / selling
    :param exercise_cost: account for exercise cost
    :param premium_premium: account for cost of purchase
    """
    x = price_range(L)
    yte = dte / 365
    duration = yte - exercise / 365

    plt.figure(figsize=(16, 8))
    call_premium = vanilla_option1(1, call_strike, yte, r, sigma, option=1)
    put_premium = vanilla_option1(1, put_strike, yte, r, sigma, option=2)
    premium = (call_size * call_premium + put_size * put_premium) * premium_premium
    option = exercise_cost * option_pnl(x, exercise, call_strike, put_strike, call_size, put_size) - premium
    lp = lp_pnl(L, x)
    maximum_loss = np.min(lp + option)
    apr = APR(L, maximum_loss, duration, premium)

    # 中文显示
    # plt.rcParams['font.sans-serif'] = ['SimHei']
    # plt.rcParams['axes.unicode_minus'] = False
    # plt.xlabel("相对价格", fontsize=12)
    # plt.ylabel("相对盈亏", fontsize=12)
    # plt.title("收益曲线", fontsize=12)
    # plt.plot(x, lp, label='{}倍杠杆LP'.format(L))
    # plt.plot(x, option,
    #          label='{:1f}天后到期，到期前{:1f}天行权，{:.2f}个Call行权价{:.2f}，{:.2f}个Put行权价{:.2f}\n '
    #                'Call单价{:.3f}，Put单价{:.3f}，隐含波动率{:.1%}'
    #          .format(dte, exercise, call_size, call_strike, put_size, put_strike, call_premium, put_premium, sigma))
    # plt.plot(x, lp + option,
    #          label='组合收益，最大回撤:{:.2%}，权利金:{:.3f}，最低APR:{:.2%}'.format(maximum_loss, premium, apr))

    plt.xlabel("Price relative to entry", fontsize=12)
    plt.ylabel("Relative PnL", fontsize=12)
    plt.title("Profit and loss", fontsize=12)
    plt.plot(x, lp, label='Farming at {} leverage'.format(L))
    plt.plot(x, option,
             label='{:.1f} days to expiration, exercise {:.1f} days before expiration\n'
                   '{:.2f} call strike at {:.2f}, {:.2f} put strike at {:.2f}\n'
                   ' call premium {:.3f}, put premium {:.3f}, IV {:.1%}'
             .format(dte, exercise, call_size, call_strike, put_size, put_strike, call_premium, put_premium, sigma))
    plt.plot(x, lp + option, label='Total PnL, maximum drawback: {:.2%}, total premium: {:.3f}, minimum APR: {:.2%}'
             .format(maximum_loss, premium, apr))
    plt.legend(loc="best", prop={'size': 12})
    plt.grid(linestyle='--')
    plt.show()
