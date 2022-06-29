import matplotlib.pyplot as plt
import numpy as np
from option_pricing import vanilla_option

if __name__ == '__main__':
    plt.figure(figsize=(16, 8))
    r = 0.05
    sigma = 1.
    T = 30
    Tr = 7

    plt.xlabel("S/K", fontsize=14)
    x = np.arange(0.01, 2, 0.01)

    plt.ylabel("PnL/K", fontsize=14)
    plt.title("PnL of Call Option", fontsize=16)
    option = vanilla_option(x, 1, Tr / 365, r, 0, sigma, 1)
    premium = vanilla_option(1, 1, Tr / 365, r, 0, sigma, 1)
    plt.plot(x, option - premium, label=f'Entry = Strike \n DTE={Tr} d, {r=:.0%}, {sigma=:.0%}')

    # plt.ylabel("Premium/K", fontsize=14)
    # plt.title("Premium of Uniswap v3 LP Option", fontsize=16)
    # premium = (1. - np.exp(-r * T / 365)) + vanilla_option(x, 1, (T + Tr) / 365, r, 0, sigma, 2) \
    #           - vanilla_option(x, 1, Tr / 365, r, 0, sigma, 2)
    # plt.plot(x, premium, label=f'{Tr=} d, {T=} d, {r=:.0%}, {sigma=:.0%}')

    # plt.ylabel("PnL/K", fontsize=14)
    # plt.title("PnL of Uniswap v3 LP Option", fontsize=16)
    # option = vanilla_option(x, 1, Tr / 365, r, 0, sigma, 2) \
    #          - np.exp(r * T / 365) * vanilla_option(1, 1, (T + Tr) / 365, r, 0, sigma, 2)
    # premium = (np.exp(r * T / 365) - 1.) + np.exp(r * T / 365) * vanilla_option(1, 1, (T + Tr) / 365, r, 0, sigma, 2)
    # plt.plot(x, option, label=f'Entry = Strike \n {Tr=} d, {T=} d, {r=:.0%}, {sigma=:.0%}')
    # plt.plot(x, - np.ones_like(x) * premium, label=f'Premium={premium:.3f}')

    # plt.xlabel("T/day", fontsize=14)
    # plt.ylabel("Premium/K", fontsize=14)
    # x = np.arange(0, 60, 0.001)
    # plt.title("Premium of Uniswap v3 LP Option", fontsize=16)
    # premium = vanilla_option(1, 1, x / 365, r, 0, sigma, 1) - vanilla_option(1, 1, 0, r, 0, sigma, 1)
    # plt.plot(x, premium, label=f'ATM, {Tr=} d, {r=:.0%}, {sigma=:.0%}')

    # plt.xlabel("Tr/day", fontsize=14)
    # plt.ylabel("Premium/K", fontsize=14)
    # x = np.arange(0, 60, 0.001)
    # plt.title("Premium of Uniswap v3 LP Option", fontsize=16)
    # premium = (1. - np.exp(-r * T)) * (1. - np.exp(-r * x / 365)) \
    #           + vanilla_option(1, 1, x / 365 + T, r, 0, sigma, 1) - vanilla_option(1, 1, x / 365, r, 0, sigma, 1)
    # plt.plot(x, premium, label=f'ATM, {T=} d, {r=:.0%}, {sigma=:.0%}')

    # T = 14
    # plt.xlabel("S/K", fontsize=14)
    # plt.ylabel("PnL/K", fontsize=14)
    # x = np.arange(0.5, 1.7, 0.01)
    # plt.title("PnL of Uniswap v2 LP Straddle", fontsize=16)
    # option = 0.5 * (x - 1) - np.sqrt(x) + np.exp(r * T / 365) \
    #          - np.exp(r * T / 365) * (1. - np.exp(- r * T / 365 / 2 - T / 365 * sigma ** 2 / 8))
    # premium = np.exp(r * T / 365) * (1. - np.exp(- r * T / 365 / 2 - T / 365 * sigma ** 2 / 8))
    # plt.plot(x, option, label=f'{T=} d, {r=:.0%}, {sigma=:.0%}')
    # plt.plot(x, - np.ones_like(x) * premium, label=f'Premium={premium:.3f}')

    plt.legend(loc="best", prop={'size': 12})
    plt.grid(linestyle='--')
    plt.show()
