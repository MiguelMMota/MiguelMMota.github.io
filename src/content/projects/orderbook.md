---
title: Orderbook trader
date: 2020-05-10T00:17:00Z
tags: ["projects", "fintech", "data analysis", "ML"]
draft: false
---

### Orderbook trader

A deep learning based strategy, still in early stages of development. The goal is train a model to detect good entries/exits for short-term positions (long or short) based on fluctuations in the orderbook for a ticker. It may also use ohlc data and orderbook data from correlated symbols.
These are the main project steps:

1. gather orderbook data for a set of correlated symbols (I chose cryptocurrency symbols to start, since they're 24h/day liquid markets, and it's relatively easy to read orderbook data via the BitMex API)
2. normalize and segment data
3. train and evaluate LSTM models
4. integrate as a signal generator for the `bitmex trader` to manage holdings for this strategy

<figure style="display:inline-block; margin:0;">
    <img src="/projects/orderbook.png" alt="OrderBook for BTC/USD" style="display:block; max-width:100%; height:auto; margin-bottom:0;" />
        <figcaption style="text-align:center; margin-top:0; font-style:italic;">example OrderBook for BTC/USD</figcaption>
</figure>

#### Key points

- data reader deployed on AWS instance
- data read from BitMex API
- `tensorflow`/`keras` (with `CUDA`) for training the LSTM models
<br>
<br>
<br>