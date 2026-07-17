# Getting started with Short Interest Datasets


Source: https://support.worldquantbrain.com/hc/en-us/community/posts/25195878621975-Getting-started-with-Short-Interest-Datasets


Tips for getting started with [Short Interest](https://platform.worldquantbrain.com/data/data-sets?category=shortinterest) Datasets:

- Short Interest: Refers to the aggregate number of a specific stock's shares that have been sold short by investors but haven't yet been covered or closed out. This quantity can be denoted as either a number or a percentage.

Short Interest: Refers to the aggregate number of a specific stock's shares that have been sold short by investors but haven't yet been covered or closed out. This quantity can be denoted as either a number or a percentage.

- Assessing Price Movement: Information on short selling and short interest of stocks can help assess price movement. You can use ts_co_skewness or ts_corr to check how fields from short interest datasets move together with close or returns.

Assessing Price Movement: Information on short selling and short interest of stocks can help assess price movement. You can use ts_co_skewness or ts_corr to check how fields from short interest datasets move together with close or returns.

- Normalization for Large Cap Stocks: Many large-cap stocks have large values for fields like short sale volume. Without normalization, the result of regular time series operations on such stocks will have a lot of spikes. Hence, it is advisable to use group_rank on the input field or after some further processing.

Normalization for Large Cap Stocks: Many large-cap stocks have large values for fields like short sale volume. Without normalization, the result of regular time series operations on such stocks will have a lot of spikes. Hence, it is advisable to use group_rank on the input field or after some further processing.

Example Alpha Ideas:

- A high short interest coupled with positive news or strong earnings could induce a short squeeze, presenting an opportunity to buy and potentially profit as short sellers try to cover their positions.

- If a stock's short interest is high and it appears to be oversold, it may be an undervalued asset worthy of investment.

- An increase in short interest alongside a consistent decline in share price may suggest a downward trend, presenting a potential opportunity for short selling.

Recommended Datasets:

- [Short Interest Model](https://platform.worldquantbrain.com/data/data-sets/shortinterest2)

- [Securities Lending Files Data](https://platform.worldquantbrain.com/data/data-sets/shortinterest3)

- [Daily Price Limit Data](https://platform.worldquantbrain.com/data/data-sets/shortinterest5)

- [Fund Flow Data](https://platform.worldquantbrain.com/data/data-sets/shortinterest10)
