from combination import *
from option_pricing import *
import numba


def VMC_plot(L=3., price_precision=0.1, size_precision=0.1, dte: float = 30, exercise: float = 0, exercise_cost=1.0,
             premium_premium=1.0):
    """Plot PnL after variational search

    :param L: leverage
    :param price_precision: fineness of strike price
    :param size_precision: fineness of option size
    :param dte: days to expiration
    :param exercise: days to expiration at exercise / selling
    :param exercise_cost: account for exercise cost
    :param premium_premium: account for cost of purchase
    """
    # years to expiration
    yte = dte / 365
    # length of farming
    duration = yte - exercise / 365
    print(dte, exercise)

    result = VMC(L, price_precision, size_precision, dte, exercise, exercise_cost, premium_premium)
    best_call_strike = result[0]
    best_call_size = result[1]
    best_put_strike = result[2]
    best_put_size = result[3]

    # x = price_range(L)
    # call_premium = vanilla_option1(1, best_call_strike, yte, r, sigma, option=1)
    # put_premium = vanilla_option1(1, best_put_strike, yte, r, sigma, option=2)
    # premium = (best_call_size * call_premium + best_put_size * put_premium) * premium_premium
    # option = exercise_cost * option_pnl(x, exercise, best_call_strike, best_put_strike, best_call_size,
    #                                     best_put_size) - premium
    # lp = lp_pnl(L, x)
    # maximum_loss = np.min(lp + option)
    # apr = APR(L, maximum_loss, duration, premium)
    # print(best_call_strike, best_call_size, best_put_strike, best_put_size, maximum_loss, premium, apr)

    plot_combo(L, best_call_strike, best_call_size, best_put_strike, best_put_size, dte, exercise, exercise_cost,
               premium_premium)


@numba.jit(nopython=True, cache=True)
def VMC(L, price_precision=0.1, size_precision=0.1, dte: float = 30, exercise: float = 0, exercise_cost=1.0,
        premium_premium=1.0):
    """Return optimal option combination after variational search

    :param L: leverage
    :param price_precision: fineness of strike price
    :param size_precision: fineness of option size
    :param dte: days to expiration
    :param exercise: days to expiration at exercise / selling
    :param exercise_cost: account for exercise cost
    :param premium_premium: account for cost of purchase
    """
    x = price_range(L)
    # parameters = []
    yte = dte / 365
    # length of farming
    duration = yte - exercise / 365
    print(dte, exercise)
    best_apr = - 1.0
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
                    call_premium = vanilla_option1(1, call_strike, yte, r, sigma, option=1)
                    put_premium = vanilla_option1(1, put_strike, yte, r, sigma, option=2)
                    premium = (call_size * call_premium + put_size * put_premium) * premium_premium
                    # call = vanilla_option(x, call_strike, exercise, r, sigma, option='call')
                    # put = vanilla_option(x, put_strike, exercise, r, sigma, option='put')
                    option = exercise_cost * option_pnl(x, exercise, call_strike, put_strike, call_size,
                                                        put_size) - premium
                    lp = lp_pnl(L, x)
                    maximum_loss = np.min(lp + option)
                    apr = APR(L, maximum_loss, duration, premium)
                    # group previous lines in one function
                    # result = vmcstep(L, x, call_strike, put_strike, call_size, put_size, yte, exercise, exercise_cost,
                    # premium_premium)
                    if apr > best_apr:
                        best_call_strike = call_strike
                        best_call_size = call_size
                        best_put_strike = put_strike
                        best_put_size = put_size
                        best_apr = apr
                    # parameters.append({'call_strike': call_strike, 'call_size': call_size, 'put_strike': put_strike,
                    #                    'put_size': put_size, 'maximum_loss': result[0], 'premium': result[1],
                    #                    'apr': result[2]})
    # parameters.sort(key=lambda x: x['apr'], reverse=True)
    print('Crude search finished.')
    # for n in range(3):
    #     print(parameters[n])
    # first_call_strike = parameters[0]['call_strike']
    # first_put_strike = parameters[0]['put_strike']
    # first_call_size = parameters[0]['call_size']
    # first_put_size = parameters[0]['put_size']
    first_call_strike = best_call_strike
    first_put_strike = best_put_strike
    first_call_size = best_call_size
    first_put_size = best_put_size
    # parameters = []
    for call_strike in np.arange(first_call_strike - price_precision, first_call_strike + 1.1 * price_precision,
                                 price_precision / 10):
        # Volatility smile.
        if call_strike < 0.795 and premium_premium == 1.:
            continue
        for put_strike in np.arange(first_put_strike - price_precision, first_put_strike + 1.1 * price_precision,
                                    price_precision / 10):
            if put_strike > 1.205 and premium_premium == 1.:
                continue
            for call_size in np.arange(first_call_size - size_precision, first_call_size + 1.1 * size_precision,
                                       size_precision / 10):
                # Only long call
                if call_size < 0:
                    continue
                for put_size in np.arange(first_put_size - size_precision, first_put_size + 1.1 * size_precision,
                                          size_precision / 10):
                    # Only long put
                    if put_size < 0:
                        continue
                    call_premium = vanilla_option1(1, call_strike, yte, r, sigma, option=1)
                    put_premium = vanilla_option1(1, put_strike, yte, r, sigma, option=2)
                    premium = (call_size * call_premium + put_size * put_premium) * premium_premium
                    # call = vanilla_option(x, call_strike, exercise, r, sigma, option='call')
                    # put = vanilla_option(x, put_strike, exercise, r, sigma, option='put')
                    option = exercise_cost * option_pnl(x, exercise, call_strike, put_strike, call_size,
                                                        put_size) - premium
                    lp = lp_pnl(L, x)
                    maximum_loss = np.min(lp + option)
                    apr = APR(L, maximum_loss, duration, premium)
                    # group previous lines in one function
                    # result = vmcstep(L, x, call_strike, put_strike, call_size, put_size, yte, exercise,  exercise_cost,
                    # premium_premium)
                    if apr > best_apr:
                        best_call_strike = call_strike
                        best_call_size = call_size
                        best_put_strike = put_strike
                        best_put_size = put_size
                        best_apr = apr
                    # parameters.append({'call_strike': call_strike, 'call_size': call_size, 'put_strike': put_strike,
                    #                    'put_size': put_size, 'maximum_loss': result[0], 'premium': result[1],
                    #                    'apr': result[2]})
    # parameters.sort(key=lambda x: x['apr'], reverse=True)
    print('Fine search finished.')
    # for n in range(3):
    #     print(parameters[n])
    # final_call_strike = parameters[0]['call_strike']
    # final_put_strike = parameters[0]['put_strike']
    # final_call_size = parameters[0]['call_size']
    # final_put_size = parameters[0]['put_size']
    result = np.asfarray([best_call_strike, best_call_size, best_put_strike, best_put_size])
    return result


@numba.jit(nopython=True, cache=True)
# @numba.vectorize("float64(float64, float64, float64, float64, float64,, float64 float64, float64, float64)", nopython=True)
# @numba.jit("(float64, float64[:], float64, float64, float64, float64, float64, float64, float64)", nopython=True)
def vmcstep(L, x, call_strike, put_strike, call_size, put_size, yte, exercise, exercise_cost, premium_premium):
    duration = yte - exercise / 365
    call_premium = vanilla_option1(1, call_strike, yte, r, sigma, option=1)
    put_premium = vanilla_option1(1, put_strike, yte, r, sigma, option=2)
    premium = (call_size * call_premium + put_size * put_premium) * premium_premium
    # call = vanilla_option(x, call_strike,  yte, r, sigma, 1)
    # put = vanilla_option(x, put_strike,  yte, r, sigma, 2)
    # option = exercise_cost * (call_size * call + put_size * put) - premium
    option = exercise_cost * option_pnl(x, exercise, call_strike, put_strike, call_size, put_size) - premium
    lp = lp_pnl(L, x)
    maximum_loss = np.min(lp + option)
    apr = APR(L, maximum_loss, duration, premium)
    result = np.asfarray([maximum_loss, premium, apr])
    return result
