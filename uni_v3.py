import matplotlib.pyplot as plt
import numpy as np
from option_pricing import vanilla_option

if __name__ == '__main__':
    plt.figure(figsize=(16, 8))
    r = 0.05
    T = 30
    Tr = 14

    plt.xlabel("S/K", fontsize=14)
    x = np.arange(0.01, 2, 0.01)

    # plt.ylabel("Premium/K", fontsize=14)
    # plt.title("Premium of Uniswap v3 LP Option", fontsize=16)
    # option = (1. - np.exp(-r * T / 365)) + vanilla_option(x, 1, 1./365*(T+Tr), r, 0, 1, 2) \
    #          - vanilla_option(x, 1, 1./365*Tr, r, 0, 1, 2)
    # plt.plot(x, option, label=f'Tr={Tr}, T={T} d, r=0.05, sigma=1')

    # plt.ylabel("PnL/K", fontsize=14)
    # plt.title("PnL of Uniswap v3 LP Option", fontsize=16)
    # option = vanilla_option(x, 1, Tr, r, 0, 1, 2) - np.exp(r * T) * vanilla_option(1, 1, Tr+T, r, 0, 1, 2)
    # premium = (np.exp(r * T / 365) - 1.) + np.exp(r * T / 365) * vanilla_option(1, 1, 1./365*(T+Tr), r, 0, 1, 2)
    # plt.plot(x, option, label='Entry = Strike \n Tr=7 d, T=30 d, r=0.05, sigma=1')
    # plt.plot(x, - np.ones_like(x) * premium, label=f'Premium={premium:.3f}')

    # plt.xlabel("T/day", fontsize=14)
    # plt.ylabel("Premium/K", fontsize=14)
    # x = np.arange(0, 60, 0.001)
    # plt.title("Premium of Uniswap v3 LP Option", fontsize=16)
    # option = vanilla_option(1, 1, x/365, r, 0, 1, 1) - vanilla_option(1, 1, 0, r, 0, 1, 1)
    # plt.plot(x, option, label='ATM, Tr=0, r=0.05, sigma=1')

    # plt.xlabel("Tr/day", fontsize=14)
    # plt.ylabel("Premium/K", fontsize=14)
    # x = np.arange(0, 60, 0.001)
    # plt.title("Premium of Uniswap v3 LP Option", fontsize=16)
    # option = (1. - np.exp(-r * T)) * (1. - np.exp(-r * x/365)) + vanilla_option(1, 1, x/365 + T, r, 0, 1, 1) \
    #     - vanilla_option(1, 1, x/365, r, 0, 1, 1)
    # plt.plot(x, option, label='ATM, T=14, r=0.05, sigma=1')

    # T = 14. / 365
    # plt.xlabel("S/K", fontsize=14)
    # plt.ylabel("PnL/K", fontsize=14)
    # x = np.arange(0.5, 1.7, 0.01)
    # plt.title("PnL of Uniswap v2 LP Straddle", fontsize=16)
    # option = np.exp(r*T) - np.sqrt(x) - np.exp(r*T) * (1. - np.exp(- r*T/2 - T/8)) + 0.5 * (x-1)
    # premium = np.exp(r*T) * (1. - np.exp(- r*T/2 - T/8))
    # plt.plot(x, option, label='T=14 d, r=0.05, sigma=1')
    # plt.plot(x, - np.ones_like(x) * premium, label=f'Premium={premium:.3f}')

    plt.legend(loc="best", prop={'size': 12})
    plt.grid(linestyle='--')
    plt.show()
