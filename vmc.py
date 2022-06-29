from combination import *


def VMC_plot(L=3., price_precision=0.1, size_precision=0.1, dte: float = 30, exercise: float = 0, exercise_cost=1.0,
             premium_premium=1.0):
    """Plot PnL after variational search

    :param L: leverage
    :param price_precision: fineness of strike price
    :param size_precision: fineness of option size
    :param dte: days to expiration
    :param exercise: days to expiration at exercise / selling
    :param exercise_cost: account for cost of exercise due to bad liquidity and fees
    :param premium_premium: account for cost of purchase due to bad liquidity and fees
    """
    # years to expiration
    yte = dte / 365
    # length of farming
    duration = yte - exercise / 365
    # print(dte, exercise)

    result = VMC(L, price_precision, size_precision, dte, exercise, exercise_cost, premium_premium)
    best_call_strike = result[0]
    best_call_size = result[1]
    best_put_strike = result[2]
    best_put_size = result[3]

    x = price_range(L)
    call_premium = vanilla_option(np.ones(1), best_call_strike, yte, r, q, sigma, 1)[0]
    put_premium = vanilla_option(np.ones(1), best_put_strike, yte, r, q, sigma, 2)[0]
    premium = (best_call_size * call_premium + best_put_size * put_premium) * premium_premium
    option = exercise_cost * option_pnl(x, exercise, best_call_strike, best_put_strike, best_call_size,
                                        best_put_size) - premium
    lp = lp_pnl(L, x)
    maximum_loss = np.min(lp + option)
    apr = APR(L, maximum_loss, duration, premium)
    # print(best_call_strike, best_call_size, best_put_strike, best_put_size, maximum_loss, premium, apr)

    plot_combo(L, best_call_strike, best_call_size, best_put_strike, best_put_size, dte, exercise, exercise_cost,
               premium_premium)


@numba.jit("float64[:](float64, float64, float64, float64, float64, float64, float64)", nopython=True, cache=True)
def VMC(L, price_precision=0.1, size_precision=0.1, dte: float = 30, exercise: float = 0, exercise_cost=1.0,
        premium_premium=1.0):
    """Return optimal option combination after variational search

    :param L: leverage
    :param price_precision: fineness of strike price
    :param size_precision: fineness of option size
    :param dte: days to expiration
    :param exercise: days to expiration at exercise / selling
    :param exercise_cost: account for cost of exercise due to bad liquidity and fees
    :param premium_premium: account for cost of purchase due to bad liquidity and fees
    """
    x = price_range(L)
    yte = dte / 365
    # length of farming
    duration = yte - exercise / 365

    strats = np.full((3, 5), -1.)
    for call_strike in np.arange(0.5, 1.5 + price_precision, price_precision):
        # Volatility smile.
        if call_strike < 0.795 and premium_premium == 1.:
            continue
        for put_strike in np.arange(0.5, 1.5 + price_precision, price_precision):
            # Volatility smile.
            if put_strike > 1.205 and premium_premium == 1.:
                continue
            for call_size in np.arange(0, 2 + size_precision, size_precision):
                for put_size in np.arange(0, 2 + size_precision, size_precision):
                    call_premium = vanilla_option(np.ones(1), call_strike, yte, r, q, sigma, 1)[0]
                    put_premium = vanilla_option(np.ones(1), put_strike, yte, r, q, sigma, 2)[0]
                    premium = (call_size * call_premium + put_size * put_premium) * premium_premium
                    option = exercise_cost * option_pnl(x, exercise, call_strike, put_strike, call_size,
                                                        put_size) - premium
                    lp = lp_pnl(L, x)
                    maximum_loss = np.min(lp + option)
                    apr = APR(L, maximum_loss, duration, premium)
                    i = strats.T[4].argmin()
                    if apr > strats.T[4][i]:
                        strats[i] = [call_strike, call_size, put_strike, put_size, apr]
    print('Crude search finished.')

    for i in np.arange(strats.shape[0]):
        strat = strats[i]
        temp = np.full((3, 5), -1.)
        for call_strike in np.arange(strat[0] - price_precision, strat[0] + 1.1 * price_precision,
                                     price_precision / 10):
            # Volatility smile.
            if call_strike < 0.795 and premium_premium == 1.:
                continue
            for put_strike in np.arange(strat[2] - price_precision, strat[2] + 1.1 * price_precision,
                                        price_precision / 10):
                if put_strike > 1.205 and premium_premium == 1.:
                    continue
                for call_size in np.arange(strat[1] - size_precision, strat[1] + 1.1 * size_precision,
                                           size_precision / 10):
                    # Only long call
                    if call_size < 0:
                        continue
                    for put_size in np.arange(strat[3] - size_precision, strat[3] + 1.1 * size_precision,
                                              size_precision / 10):
                        # Only long put
                        if put_size < 0:
                            continue
                        call_premium = vanilla_option(np.ones(1), call_strike, yte, r, q, sigma, 1)[0]
                        put_premium = vanilla_option(np.ones(1), put_strike, yte, r, q, sigma, 2)[0]
                        premium = (call_size * call_premium + put_size * put_premium) * premium_premium
                        option = exercise_cost * option_pnl(x, exercise, call_strike, put_strike, call_size,
                                                            put_size) - premium
                        lp = lp_pnl(L, x)
                        maximum_loss = np.min(lp + option)
                        apr = APR(L, maximum_loss, duration, premium)
                        j = temp.T[4].argmin()
                        if apr > temp.T[4][j]:
                            temp[j] = [call_strike, call_size, put_strike, put_size, apr]
        j = temp.T[4].argmax()
        strats[j] = temp[j]
    print('Fine search finished.')
    i = strats.T[4].argmax()
    result = strats[i]
    return result
