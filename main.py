import time
import timeit
import numpy as np
from vmc import *
from combination import *

if __name__ == '__main__':
    # days to expiration when opening
    dte: float = 60
    # days to expiration at exercise / selling
    exercise: float = 30

    # VMC_plot(L=2.5, price_precision=0.1, size_precision=0.1, dte=dte, exercise=exercise, exercise_cost=1,
    #          premium_premium=1)
    print(timeit.timeit(
        'VMC_plot(L=2.5, price_precision=0.1, size_precision=0.1, dte=dte, exercise=exercise, exercise_cost=1, premium_premium=1)',
        globals=globals(), number=5) / 5)

    # print(timeit.timeit('VMC(3, price_precision=0.1, size_precision=0.1, dte=27, exercise_cost=1, premium_premium=1)'
    #                     , globals=globals(), number=50)/50)
    x = price_range(3.)
    # print(timeit.timeit('vanilla_option(x, 1.,  30. / 365, r, q, sigma, 1)', globals=globals(), number=100000))

    # Options are not available at any strike and any dte. Use the following to adjust and see.
    spot = 530.
    # print(vanilla_option([spot], 58000, dte/365, r, q, sigma, 1)[0])
    # print(vanilla_option([spot], 58000, dte/365, r, q, sigma, 2)[0])
    cs = 700.
    ps = 700.
    # print("Call Strike {}, Put Strike {}".format(cs, ps))
    # print("Call price {}".format(vanilla_option([spot],  cs, dte /365, r, q, sigma, 1))[0])
    # print("Put price {}".format(vanilla_option([spot],  ps, dte/365, r, q, sigma, 2))[0])
    # plot_combo(L=3, call_strike=4040/3470, call_size=0.25, put_strike=3080/3470, put_size=0.25, dte=dte,
    #            exercise_cost=1., premium_premium=1.)
