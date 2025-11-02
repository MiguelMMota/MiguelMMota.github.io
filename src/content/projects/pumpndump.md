---
title: Pump n' Dump
date: 2019-10-21T00:17:00Z
tags: ["projects", "sentiment analysis", "ML"]
draft: false
---

### Pump n' Dump

My most ambitious project yet. Prompted by an article on the potential correlation between reddit activity and stock price movements, I wondered if a similar relationship could exist in the fintwit community. These were the main steps:

1. gather stock daily price, volume, and twitter data for 2016-2020 
2. train a `scikit` model for stock sentiment analysis on a rather small but representative set of tweets reflecting various opinions on the outlook of certain stocks.
3. set model targets based on stock performance after a short period of time.
4. create various features based on olhc data and twitter activity, and select a subset of those with low correlation and high relevance, to reduce system complexity. 
5. preprocess the data into normalized input sequences, avoiding bias
6. use smote oversampling to get a more even distribution of targets. 
7. test several variations of the model against a separate dataset, and rank them by their F-score, based on the confusion matrix. 
8. integrate with brokerage account for automatic order placement
9. automate entire workflow to run continuously 

#### Key points

- Text sentiment analysis for stock tweets
- `twint` for tweet scraping  
- `ib_insync` for assynchronous interfacing with Interactive Brokers account
- preliminary analysis: logistic regression, pca, factor analysis
- `tensorflow`/`keras` (with `CUDA`) for training the LSTM model
- efficiency is an important consideration for this project, as reading and processing price, volume, and twitter data for thousands of stocks before feeding the data into the model for projections could take long enough that one wouldn't be able to act on the output.
<br>
<br>
<br>