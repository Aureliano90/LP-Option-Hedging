import matplotlib.pyplot as plt
from option_pricing import *

# annualized volatility
sigma = 0.8
# risk-free interest rate on stablecoin
r = 0.1
# risk-free interest rate on crypto
q = 0.005

# debt type
# B for borrowing crypto, U for borrowing stablecoin, B+U for pseudo neutral strategy
# borrow = 'B'
# borrow = 'U'
borrow = 'B+U'

# liquidation debt ratio
LTVf = 0.83

# APR from DEX without leverage including trading fees and liquidity mining rewards
apr_dex = 0.155
# APR from yield aggregators for borrowing crypto
# APR in ALPHA/ALPACA minus borrowing interest
apr_farm_B = 0.044 - 0.025
# APR from yield aggregators for borrowing stablecoin
# APR in ALPHA/ALPACA minus borrowing interest
apr_farm_U = 0.019 - 0.2


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


@numba.vectorize("float64(float64, float64, float64, float64, float64, float64)", nopython=True, cache=True)
# @numba.jit("float64[:](float64[:], float64, float64, float64, float64, float64)", nopython=True, cache=True)
def option_pnl(x, exercise: float, call_strike, put_strike, call_size, put_size):
    """Payoff of the option combination

    :param x: underlying price
    :param exercise: days to expiration at exercise / selling
    :param call_strike:
    :param put_strike:
    :param call_size:
    :param put_size:
    :return: pnl
    """
    call = vanilla_option(x, call_strike, exercise / 365, r, q, sigma, 1)
    put = vanilla_option(x, put_strike, exercise / 365, r, q, sigma, 2)
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
        if L < 2:
            print("Leverage must not be less than 2 for pseudo neutral strategy.")
            return 0.
        else:
            # a is the ratio of initial capital that is used to open a farming position that borrows crypto.
            # 1-a is used to open a farming position that borrows stablecoin.
            # a <= 1
            # delta = 0 = a * (L/2 - L + 1) + (1 - a) * L/2 = -aL + a + L/2
            a = L / 2 / (L - 1)

            return (a * apr_farm_B + (1 - a) * apr_farm_U) * (L - 1) / (1 + premium) + (
                    apr_dex * L + maximum_loss / duration) / (1 + premium)
    else:
        print("Specify debt type.")
        return 0.0


def plot_combo(L, call_strike, call_size, put_strike, put_size, dte: float = 30, exercise: float = 0, exercise_cost=1.0,
               premium_premium=1.0):
    """Plot PnL graphs

    :param L: leverage
    :param call_strike:
    :param call_size:
    :param put_strike:
    :param put_size:
    :param dte: days to expiration
    :param exercise: days to expiration at exercise / selling
    :param exercise_cost: account for exercise cost
    :param premium_premium: account for cost of purchase
    """
    x = price_range(L)
    yte = dte / 365
    duration = yte - exercise / 365

    plt.figure(figsize=(16, 8))
    call_premium = vanilla_option(np.ones(1), call_strike, yte, r, q, sigma, 1)[0]
    put_premium = vanilla_option(np.ones(1), put_strike, yte, r, q, sigma, 2)[0]
    premium = (call_size * call_premium + put_size * put_premium) * premium_premium
    option = exercise_cost * option_pnl(x, exercise, call_strike, put_strike, call_size, put_size) - premium
    lp = lp_pnl(L, x)
    maximum_loss = np.min(lp + option)
    apr = APR(L, maximum_loss, duration, premium)

    # 中文显示
    # plt.rcParams['font.sans-serif'] = ['SimHei']
    # plt.rcParams['axes.unicode_minus'] = False
    # plt.title("杠杆挖矿，期权，及其组合", fontsize=16)
    # plt.xlabel("现价相对开仓价", fontsize=14)
    # plt.ylabel("相对本金盈亏", fontsize=14)
    # assert borrow in ['B', 'U', 'B+U']
    # if borrow == 'B':
    #     debt = '借币'
    # elif borrow == 'U':
    #     debt = '借U'
    # else:
    #     a = L / 2 / (L - 1)
    #     debt = f'{a:.2f}借币，{1-a:.2f}借U'
    # plt.plot(x, lp, label=f'{L}倍杠杆LP，' + debt)
    # plt.plot(x, option, label=f'{dte:.1f}天后到期，到期前{exercise:.1f}天行权，{call_size:.2f}个Call行权价{call_strike:.2f}，'
    #                           f'{put_size:.2f}个Put行权价{put_strike:.2f}\n Call单价{call_premium:.3f}，'
    #                           f'Put单价{put_premium:.3f}，隐含波动率{sigma:.1%}')
    # plt.plot(x, lp + option, label=f'组合收益，最大回撤:{maximum_loss:.2%}，权利金:{premium:.3f}，最低APR:{apr:.2%}')

    plt.title("Leveraged yield farming, options, and their combination", fontsize=16)
    plt.xlabel("Price relative to entry", fontsize=14)
    plt.ylabel("Relative PnL", fontsize=14)
    assert borrow in ['B', 'U', 'B+U']
    if borrow == 'B':
        debt = 'borrowing crypto'
    elif borrow == 'U':
        debt = 'borrowing stable'
    else:
        a = L / 2 / (L - 1)
        debt = f'{a:.2f} borrowing crypto, {1 - a:.2f} borrowing stable'
    plt.plot(x, lp, label=f'Farming at {L} leverage, ' + debt)
    plt.plot(x, option,
             label=f'{dte:.1f} days to expiration, exercise {exercise:.1f} days before expiration\n'
                   f'{call_size:.2f} call strike at {call_strike:.2f}, {put_size:.2f} put strike at {put_strike:.2f}\n'
                   f' call premium {call_premium:.3f}, put premium {put_premium:.3f}, IV {sigma:.1%}')
    plt.plot(x, lp + option,
             label=f'Total PnL, maximum drawback: {maximum_loss:.2%}, total premium: {premium:.3f},'
                   f' minimum APR: {apr:.2%}')

    plt.gca().yaxis.set_major_formatter('{x:.0%}')
    plt.legend(loc="best", prop={'size': 12})
    plt.grid(linestyle='--')
    plt.show()
