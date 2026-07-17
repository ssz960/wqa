# Getting started with News Datasets


Source: https://support.worldquantbrain.com/hc/en-us/community/posts/25238147879319-Getting-started-with-News-Datasets


Tips for getting started with [News](https://platform.worldquantbrain.com/data/data-sets?category=news) Datasets:

- News data refers to the latest financial news that leads to market changes. It can be sourced from various places including:
Financial reports, which cover earnings, investments, dividends
Analysts' recommendations, featuring expectations, ratings, opinions
Company product updates, such as new product launches or approvals
Legal events about investigations or bankruptcies

- Financial reports, which cover earnings, investments, dividends

- Analysts' recommendations, featuring expectations, ratings, opinions

- Company product updates, such as new product launches or approvals

- Legal events about investigations or bankruptcies

- Combining news and stock prices seeks to offer more comprehensive insights

- The impact of news can be significant and enduring, possibly influencing the market for a month, a quarter, or even longer. When integrated with stock prices, news data can offer a deeper understanding of market behaviors and trends.

- By carefully analyzing and utilizing news data, investors can gain valuable insights into market trends and make more informed decisions.

Examples of Alpha Ideas:

- News (or event) datasets: These datasets contain data fields regarding the change in price or volume in response to a news event. The key to success here is determining the true impact of a news story or event.

- Noise filtering: News data is expected to contain substantial amounts of noise. To filter this noise, we recommend employing operations such as winsorizing, truncating, or left/right tail filtering.

- Signal regularization: Further regularization of signals tends to improve the performance of such an Alpha. We recommend utilizing cross-sectional operations such as normalization, ranking, or vector neutralization.

- Volume change: The change in volume before and after a news event can serve as an indicator of how impactful a news story or event is on a corresponding stock (or even a sector).

- Direction of price changes: Another tip for using news data is to take note of the direction of price changes (i.e., increasing or decreasing) around an event. Associating these directions with closing prices or returns can help integrate the impact of news on stock prices.

Recommended Datasets:

- [Dow Jones News Analytics Data](https://platform.worldquantbrain.com/data/data-sets/news3)

- [News Feed Analytics Data](https://platform.worldquantbrain.com/data/data-sets/news5)

- [PR Edition Data](https://platform.worldquantbrain.com/data/data-sets/news17)

- [Web Sources News Sentiment Data](https://platform.worldquantbrain.com/data/data-sets/news20)

- [News Analytics on Equities](https://platform.worldquantbrain.com/data/data-sets/news31)

- [Relevant News Analytics Data](https://platform.worldquantbrain.com/data/data-sets/news46)
