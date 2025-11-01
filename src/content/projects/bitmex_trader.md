---
title: Bitmex trader 
date: 2021-04-29T00:17:00Z
tags: ["projects"]
draft: true
---

### Bitmex trader

An automated portfolio manager integrated with the Bitmex crypto exchange for trade execution and with TradingView for signal generation.

Signals are received assynchronously via a web app, and processed according to a `json` config file for the portfolio. The portfolio manager:

- decides whether to act on the signal received based on current exposure
- determines position size and order types to use
- sets stop loss and profit target orders, if applicable to the strategy 
<br>
<br>
{{< figure src="/projects/bitmex_trader_sequence_diagram.png" >}}

#### Key points
- Written in Python
- `Quart` for REST API
- `rpyc` for communication between services

For more information on the trading signal generation, see the `TradingView strats` project
<br>
<br>
<br>