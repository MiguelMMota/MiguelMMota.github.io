---
title: Reddit tracker 
date: 2020-04-29T00:17:00Z
tags: ["projects", "data analysis"]
draft: false
---

### Reddit tracker

Following the $GME hysteria which started in early 2021, and the ensuing public discussion on the impact of the activity in certain reddit forums in the stock market, I was curious to research the topic myself.

I built a small solution to read data from specific subreddits, and analyse various metrics related to public sentiment and activity.

The project interfaces with the Google Sheets API to produce daily reports on the stocks that stand out. For example, I was curious to look at tickers with:

- High activity (many posts and/or comments)
- Polarized sentiment
- High activity surge/decline from previous day and/or recent days
- High sentiment switch from previous day and/or recent days

**Disclaimer:** I wrote this purely for research purposes, and didn't share any of this data (despite it being public), or use it to initiate any positions.


#### Key points
- Written in Python
- `praw` for reddit crawling
- `gspread` for writing to excel sheets
- `spacy`/`sklearn` for custom sentiment analyser
<br>
<br>
<br>