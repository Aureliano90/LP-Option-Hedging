import matplotlib.pyplot as plt
import numpy as np
from option_pricing import vanilla_option


if __name__ == '__main__':
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.figure(figsize=(16, 8))
    plt.title("收益曲线", fontsize=12)
    plt.xlabel("相对价格", fontsize=12)

    # plt.ylabel("相对法币盈亏", fontsize=12)
    # x = np.arange(0, 2, 0.01)
    # for L in range(1, 4):
    #     lp = L * np.sqrt(x) - L * x + x - 1
    #     plt.plot(x, lp, label='{}倍杠杆LP'.format(L))

    plt.ylabel("相对盈亏", fontsize=12)
    x = np.arange(0.5, 2, 0.01)
    # for L in range(1, 4):
    #     lp = L * np.sqrt(x) - L - 0.5 * L * (x - 1)
    #     plt.plot(x, lp, label='{}倍杠杆LP'.format(L))
    L = 2.5
    lp = L / np.sqrt(x) - L + 1.25 * (x - 1) / x
    plt.plot(x, lp, label='{}倍杠杆LP'.format(L))

    plt.legend(loc="best",  prop={'size': 12})
    plt.grid(linestyle='--')
    plt.show()
