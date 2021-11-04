import matplotlib.pyplot as plt
import numpy as np
from option_pricing import vanilla_option


if __name__ == '__main__':
    plt.figure(figsize=(16, 8))

    # plt.rcParams['font.sans-serif'] = ['SimHei']
    # plt.rcParams['axes.unicode_minus'] = False
    # plt.title("杠杆挖矿收益曲线", fontsize=16)
    # plt.xlabel("现价相对开仓价", fontsize=14)
    plt.title("Profit and loss of leveraged yield farming", fontsize=16)
    plt.xlabel("Price relative to entry", fontsize=14)

    # plt.ylabel("以法币计相对盈亏", fontsize=14)
    # plt.ylabel("Relative PnL in stablecoin", fontsize=14)
    # x = np.arange(0, 2, 0.01)
    # for L in range(1, 4):
    #     lp = L * np.sqrt(x) - L * x + x - 1
    #     plt.plot(x, lp, label='{}倍杠杆借币'.format(L))
    #     plt.plot(x, lp, label='Borrow crypto at {} leverage'.format(L))

    # plt.ylabel("以法币计相对盈亏", fontsize=14)
    plt.ylabel("Relative PnL in stablecoin", fontsize=14)
    L = 2
    x = np.arange(0, 4, 0.01)
    lp = L * (np.sqrt(x) - 1)
    # plt.plot(x, lp, label='{}倍杠杆借U'.format(L))
    plt.plot(x, lp, label='Borrow stablecoin at {} leverage'.format(L))

    plt.legend(loc="best",  prop={'size': 12})
    plt.grid(linestyle='--')
    plt.show()
