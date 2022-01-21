# LP-Option-Hedging

### Description

A Python program to analyze leveraged liquidity mining/yield
farming[[1]](https://github.com/Aureliano90/LP-Option-Hedging#reference) and find the optimal option strategy for
hedging impermanent loss, which may allow arbitrage. Initially written in May for my personal use. Optimized by 30x with
Numba. Restructured and added annotations to make it more approaching.

### Utility

The code may plot PnL graphs for leveraged liquidity provider (LP) positions on constant product Automated Market Maker
(AMM)[[2]](https://github.com/Aureliano90/LP-Option-Hedging#reference), like those
on [Alpha Homora](https://homora.alphafinance.io/) and [Alpaca Finance](https://www.alpacafinance.org/). It can perform
a variational search for the optimal combination of call options and put options which minimizes impermanent loss in
leveraged LP. It then plots the PnL graphs for leveraged LP, the option strategy with sizes and strike prices, and the
combination of leveraged LP and options.

The type of leveraged LP can be borrowing USD stablecoins, borrowing cryptos like BTC, ETH, and a pseudo delta neutral
combination of the two.

Parameters that need to be manually specified:

* debt type
* leverage of LP
* LTV at liquidation
* APRs on farming
* annualized volatility, risk-free interest rate for crypto and stablecoin
* days to expiration and day of exercise/reselling of European options priced by the Black-Scholes
  model[[3]](https://github.com/Aureliano90/LP-Option-Hedging#reference)

### Background

Providing liquidity on AMM is equivalent to short gamma and long theta, i.e. the LP subjects itself to impermanent loss
in exchange for trading fees and liquidity mining rewards. On the other hand, long call and long put have positive gamma
and negative theta. By virtue of the Carr–Madan formula[[4]](https://github.com/Aureliano90/LP-Option-Hedging#reference)
, a smooth function of the underlying price, in this case the payoff of leveraged LP, can be replicated by a series of
European options at continuous strikes. Hence it is possible to completely hedge leveraged LP with options. In pratice
options are not available at any strike. Moreover the volatility is not constant at all strikes due to the volatility
smile. Therefore the current program only considers a long call and a long put for hedging.

### Disclaimer

The hedging is only approximate and theoretical. The author is not responsible for any loss caused by the use of this
program. Do your own research.

### Reference

[1] [What Is Yield Farming in Decentralized Finance (DeFi)?](https://academy.binance.com/en/articles/what-is-yield-farming-in-decentralized-finance-defi)

[2] [What Is an Automated Market Maker (AMM)?](https://academy.binance.com/en/articles/what-is-an-automated-market-maker-amm)

[3] [The Black–Scholes model](https://en.wikipedia.org/wiki/Black%E2%80%93Scholes_model)

[4] [The Carr-Madan Formula](https://engineering.nyu.edu/sites/default/files/2019-01/CarrQuantFinance2001-a.pdf)

# 期权对冲流动性挖矿

### 简介

一个分析杠杆流动性挖矿并寻找最佳期权组合以对冲无常损失的Python程序，写于五月初，经Numba优化。

### 功能

给出基于恒定乘积AMM的杠杆挖矿的损益曲线，并寻找对冲无常损失的最佳期权组合，画出杠杆LP、期权组合包括张数和行权价及总仓位的损益曲线。

杠杆挖矿的类型包括借U、借币及伪中性敞口的组合。

需手动输入的参数：

* 贷款类型
* 杠杆倍数
* 清算时债务比例
* 挖矿APR
* 年化波动率、无风险利率
* 到期日、行权日

### 免责声明

程序模拟仅为理论近似，本人不对由此造成的任何损失负责。