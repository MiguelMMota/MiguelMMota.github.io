---
title: "Code Autoshop #1"
date: 2021-03-21T00:17:00Z
tags: ["projects", "fintech"]
---

Welcome to *The Python Way*'s first series: Code Autoshop! 



## The Autoshop
In this series, I'll be picking up projects and trying to improve them in some way, focusing on **very specific techniques**.

Over my years working with software engineers from various experience levels, I've improved my development process while becoming increasingly aware of common pitfalls or suboptimal practices. Note that some of these aren't necessarily *wrong* practices, but to me they're just not that great. My own personal growth as a developer combined with the fact that Python keeps evolving as a language means that some of my own earlier projects are great candidates for this experiment.

I'll be sharing documentation and code for this work as I go along. To make sure I can keep a steady pace, I'll tackle one technique at a time: one post to describe it, another to apply it to the original project. So the expected flow is:

- Introduction (this post)
- Technique #1
    - Description
    - Application
- Technique #2
    - Description
    - Application
- ...
- Conclusion

Enough of that, onto the first project!



## BitmexTrader
Some time ago, I was curious to develop an automated trading strategy for cryptocurrencies (don't worry, you don't need to be a Bitcoin or trading aficionado to follow along). After a while, I finally came up with a couple of setups that I was fairly confident in, and quickly put something together to test these strategies in a paper trading account (i.e.: with *fake* money). The [BitmexTrader](https://gitlab.com/miguel_mota/bitmextrader) repo was born (brace yourself before clicking the link, it does **not** look pretty at time of writing). 

The solution should consume HTTP requests to asynchronously manage a cryptocurrency portfolio:

- The [Quart](https://pypi.org/project/Quart/) application receives HTTP requests that represent trade signals, and relays them to a portfolio manager
- The portfolio manager is a high level abstraction on top of trading strategies:
    - single interface to the Quart app
    - additional control over strategies (e.g.: to limit overall exposure)
    - single interface with Bitmex API
- The strategies indicate to the portfolio manager how they'd like to react to the trading signal (e.g.: buy/sell 1 Bitcoin), and keep track of intermediate status of requests to the Bitmex API

Sound confusing? Well, the first step in this work will help with that: updating the documentation with [UML](https://en.wikipedia.org/wiki/Unified_Modeling_Language) diagrams to summarise the scope of the project.

*Sidenote*: for the purposes of this exercise, it's irrelevant how the signals are generated and sent to our application. In fact, the Quart app is simple, and we're interested in improving what goes on at the portfolio manager level and below. If you're interested in the signal generation part, I may do a separate series more fintech related. For now, you can check out the [TradingView](http://tradingview.com) script editor and alert system, which is what I used to generate trading signals for my strategies automatically.

## The techniques
In order to maintain a clear focus during these improvements, and for the purposes of demonstration, I'll focus on one approach at a time. This is the initial set of improvements that I'll apply:

- Planning and documentation
- Code style
- Unit tests
- Integrated tests
- Refactoring 
- More, smaller classes
- Events
- Database
- SOLID principles
- 'Pythonic' code
- Efficiency
- Static analysis
- Linting
- Auto-generated documentation
- Docker integration

To the inexperienced reader, some or even most of these steps may seem like merely additional work. To an extent, I admit I might not have opted into this exercise if not for the added educational value that it'll provide here. Also I don't want to curl up with embarassment at the thought of sharing my code in such a shameful state... 😆


![](/2021-03-21-code-autoshop-1/shame.png)


Hopefully over the next few months I'll be able to showcase how each of these approaches can incrementally add value to your projects to the point where the sum of all these changes will bring drastic improvements to code quality, resulting in a more robust product, and ultimately even faster development cycles. For myself, at least, I can tell you I cannot understate the impact that I've seen from making these practices second nature to my work.

Stay tuned for further developments!