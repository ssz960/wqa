# Getting started with Social Media Datasets


Source: https://support.worldquantbrain.com/hc/en-us/community/posts/25297889562135-Getting-started-with-Social-Media-Datasets


Tips for getting started with [Social Media](https://platform.worldquantbrain.com/data/data-sets?category=socialmedia) Datasets:

- Social media data are based on information from newspapers, news websites, Facebook, Twitter, blog posts, discussion groups, and forums.

- The data provide social sentiment as well as sentiment volume for different stocks.

- Social sentiment indicators help investors identify information in social media that could cause a stock's price to increase or decrease in the near future.

- Unlike fundamental data, these data naturally have high frequencies, which can lead to high turnovers in an alpha**.**

- To achieve reasonable margin rates, consider using the following operations: hump_decay, ts_decay_linear, and ts_decay_exp_window. However, be careful when using lookback periods greater than 63 days (i.e., one quarter) as older events may have no impact.

Example Alpha Ideas:

- Long / short stocks with positive / negative sentiment, filtering out days and stocks with low sentiment volume.

- Use sentiment volume as a proxy for market's attention to a stock. This could be used directly as a stock returns predictor or a condition in trade_when.

- For vector data fields, experiment with other vector operators like vec_max, vec_min, or vec_range to retrieve different information from the vector data rather than simply using vec_avg.

Recommended Datasets:

- [Twitter based sentiment data](https://platform.worldquantbrain.com/data/data-sets/socialmedia3)

- [Brands and Social Media Data](https://platform.worldquantbrain.com/data/data-sets/socialmedia4)

- [Lexical Breakdown Data](https://platform.worldquantbrain.com/data/data-sets/socialmedia5)

- [Social Media Data for Equity](https://platform.worldquantbrain.com/data/data-sets/socialmedia8)

- [Social Media Activity Data](https://platform.worldquantbrain.com/data/data-sets/socialmedia9)

- [Sentiment Data for Equity](https://platform.worldquantbrain.com/data/data-sets/socialmedia12)

- [Sentiment Indicators](https://platform.worldquantbrain.com/data/data-sets/socialmedia15)
