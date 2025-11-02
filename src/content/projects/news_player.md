---
title: News player
date: 2023-01-12T00:17:00Z
tags: ["projects", "fintech", "nltk"]
draft: true
---

### News player
While I was working on the 'GapUp short' strategy, I noticed that often the strong stock movements outside market hours were motivated by news articles. Many traders subscribe to services like Benzinga to react quickly to these events, and hopefully make some money by getting in ahead of the crowd.

I wondered if there was an edge in this process, and if I could create an automated strategy off of it. Here's how I went about it:

1. Analyse stocks that gapped up outside market hours, backtracking ~6 months. What kind of news were linked to the strongest reactions? How to accept only those as trading signals? 
2. Analyse several news sources against the news that may have caused these price swings. I was looking for three essential points: fast to report, doesn't miss a lot of relevant events, provides automated alerts of some kind
3. Subscribe to news alerts of my selected source, and redirect them as POST requests
4. Create web app on an AWS service to listen to and process these requests
5. Fine tune approach to trading these signals (stop loss, profit target)
6. Link with a brokerage account and implement order placement and position management 


#### Key points

- `nltk` (tokenizing, n-grams)  
- `ib_insync` for assynchronous interfacing with Interactive Brokers account
- lack of liquidity outside market hours was a strong limiting factor for this strategy 

<br>
<br>
<br>