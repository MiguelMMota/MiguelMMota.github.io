---
title: GapUp short
date: 2021-04-29T00:17:00Z
tags: ["projects"]
draft: true
---

### GapUp short
A few years ago, I was introduced to low-cap stocks. Retail traders in this space seem to design strategies based on superficial statistical analysis and little to no backtesting.

I picked a basic strategy, the 'Gap Fail' - screening low-cap stocks that gap significantly in pre-market, and short them at or near market open - and set out to analyse it.

I used QuantConnect to quickly code this strategy. Early results were encouraging, and were iteratively improved upon by fine tuning stock screening parameters such as sector, premarket volume, and min/max stock price, entry point, max loss, profit target. 

I set out to automate live execution of the strategy after fine-tuning it. This proved difficult, due to the nature of the pattern: since I was shorting low-cap stocks, it was often necessary to preemptively locate the shares to short. I couldn't find a broker with an API that allowed this process to be automated.

Eventually, I opened an account with TradeStation, and worked through their scripting language (EasyLanguage) to implement the strategy. Unfortunately, trading strategies had to be applied directly on a single stock chart, so stock selection had to be done manually.    


#### Key points

- Great backtesting results in a vacuum
- The need to locate shares to short hurt the strategy, by:
    - eliminating many promising plays: locates often failed for good shorts
    - increasing costs: share locates are often costly
    - requiring manual intervention
- In the end, I abandoned the strategy, as I wasn't interested in manual trading 

<br>
<br>
<br>