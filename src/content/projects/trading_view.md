---
title: TradingView strats
date: 2020-01-02T00:17:00Z
tags: ["projects", "fintech", "Pinescript"]
draft: false
---

### TradingView strats
TradingView is a fantastic resource for traders. It's one of my default tools for my market research.

I implemented a set of utils for my own research:

- an indicator based on the TTM squeeze
- a VWAP trading strategy
- a strategy based on catching bull flags
- a strategy based on the MACD and some EMAs
- a strategy based on the TTM squeeze and the MACD

I backtested these strategies against various tickers (I was primarily interested in cryptocurrencies), with some good results. The TTM/MACD strat, for example, yielded a 63.45% profit after commissions with a 10.46% max drawdown when applied to a XBTUSD 30min chart over a 10-month period. The Sharpe ratio was slightly low, at 0.602. 

Simply holding XBTUSD long for the same period whould have yielded returns of 78.25%, with a 62.84% max drawdown. In comparison, the TTM/MACD strat had:

- 1.23x smaller returns
- 6x smaller drawdown
- 2.19x larger holding period return (TTM/MACD strat only held a position ~37% of the time)

*Note:* this strat works best for consolidation markets, without a clear trend. Since the Bitcoin breakout in late October 2020, a simple buy-and-hold approach massively outperformed this strategy. 


#### Key points
- Implemented in Pine Script, TradingView's own scripting language
- Fully parameterized
- Automatic alerts are issued via a webhook URL, and can be consumed by a web app interfacing with a broker/exchange

<br>
<br>
<br>