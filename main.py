import time
import timeit
from option_pricing import vanilla_option1
from combination import *
from vmc import *

if __name__ == '__main__':
    VMC_plot(2.5, price_precision=0.1, size_precision=0.1, length=45, exercise_cost=1, premium_premium=1)
    # VMC_plot(3, price_precision=0.1, size_precision=0.1, length=20, exercise_cost=1, premium_premium=1)
    # print(timeit.timeit('VMC(3, price_precision=0.1, size_precision=0.1, length=27, exercise_cost=1, premium_premium=1)', globals=globals(), number=50)/50)
    # x = price_range(3.)
    # print(timeit.timeit('vanilla_option(x, 1.,  30. / 365, r, sigma, 1)', globals=globals(), number=100000))

    spot = 530.
    expiration = 30
    # print(1.05 * vanilla_option1(spot, 58000, expiration / 365, 0.05, sigma, 'call'))
    # print(1.05 * vanilla_option1(spot, 58000, expiration / 365, 0.05, sigma, 'put'))
    cs = 700.
    ps = 700.
    # print("Call Strike {}, Put Strike {}".format(cs, ps))
    # print("Call price {}".format(vanilla_option1(spot,  cs, expiration/365, r, sigma, 1)))
    # print("Put price {}".format(vanilla_option1(spot,  ps, expiration/365, r, sigma, 2)))
    # plot_combo(3, 4040/3470, 0.25, 3080/3470, 0.25, 20, 1., 1.)

    # Minimal drawdown
    # plot_combo(3, 0.85, 0.59, 0.4, 0.01, duration=15)
    # Maximal return
    # plot_combo(3, 0.85, 0.59, 0.9, 0., duration=30)
    # plot_combo(3, 0.8, 0.6, 1, 0, duration=30)
    # plot_combo(2, 0.86, 0.3, 1.2, 1.29, duration=27)
    # plot_combo(2.5, 0.99, 0.36, 1.58, 1.47, duration=30)
