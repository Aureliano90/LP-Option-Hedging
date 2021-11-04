import matplotlib.pyplot as plt
import numpy as np
from option_pricing import vanilla_option


if __name__ == '__main__':
    plt.figure(figsize=(16, 8))

    # plt.rcParams['font.sans-serif'] = ['SimHei']
    # plt.rcParams['axes.unicode_minus'] = False
    # plt.title("收益曲线", fontsize=12)
    # plt.xlabel("相对价格", fontsize=12)
    plt.title("Profit and loss", fontsize=12)
    plt.xlabel("Price relative to entry", fontsize=12)

    # plt.ylabel("相对法币盈亏", fontsize=12)
    # plt.ylabel("Relative PnL in stablecoin", fontsize=12)
    # x = np.arange(0, 2, 0.01)
    # for L in range(1, 4):
    #     lp = L * np.sqrt(x) - L * x + x - 1
    #     plt.plot(x, lp, label='借币{}倍杠杆LP'.format(L))
    #     plt.plot(x, lp, label='Borrow crypto at {} leverage'.format(L))

    plt.ylabel("Relative PnL in stablecoin", fontsize=12)
    L = 2
    x = np.arange(0, 4, 0.01)
    lp = L * (np.sqrt(x) - 1)
    plt.plot(x, lp, label='Borrow stablecoin at {} leverage'.format(L))

    plt.legend(loc="best",  prop={'size': 12})
    plt.grid(linestyle='--')
    plt.show()
