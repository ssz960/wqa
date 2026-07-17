# Creating D0 Alphas with Analyst Data


Source: https://support.worldquantbrain.com/hc/en-us/community/posts/18426256195351-Creating-D0-Alphas-with-Analyst-Data


Introduction to Analyst Data

The availability and utilization of analyst data are important for participants in the stock market. Analysts provide valuable insights and recommendations based on their expertise and research, which can influence investment decisions. By analyzing financial statements, industry trends, market conditions, and other pertinent information, analysts offer a comprehensive evaluation of companies and their stocks. This data helps investors identify potential investment opportunities, assess the risks involved, and make informed decisions. Furthermore, by providing regular updates and revisions to their estimates, analysts help investors stay updated on the performance and prospects of their investments.

Recommended/Relevant Datasets

Since Delay-0[[1]](https://support.worldquantbrain.com#_ftnref1) Alphas[[2]](https://support.worldquantbrain.com#_ftnref1) allow one to capture information in the market during market hours, it's also a good idea to try and capture signals embedded in analyst data quicker with these types of Alphas. The following are some suggested datasets and ideas you can start with when working with D0 Alphas:

- [Analyst Estimate Data for Equity (analyst4)](https://platform.worldquantbrain.com/data/data-sets/analyst4): This dataset is a useful starting point, providing details and aggregations on opinions from analysts regarding upcoming fiscal quarters and future years. If the mean of analysts' estimations is used as an approximation for the fair value of a stock, one can identify undervalued and overvalued stocks by analyzing the discrepancy between estimations and current values. However, it is important to note that the mean of estimations might not be a good proxy during periods of low consensus. Additionally, this dataset offers good coverage in all available regions.

- [Analyst Revisions Model Data (model216)](https://platform.worldquantbrain.com/data/data-sets/model216): This dataset provides a stock ranking system that assigns a daily ranking from 1 to 100 for various global stocks. A higher ranking (or an increase in ranking) is usually associated with a more positive outlook on a stock's price. Additionally, this dataset offers good coverage in all available regions.

- [Real Time Estimates (analyst16)](https://platform.worldquantbrain.com/data/data-sets/analyst16): Along with the usual estimate values, one can also find a variety of data fields within this dataset. For example, the standard deviation of estimates can be used as an indicator of high or low market consensus.

Additional tip when working with analyst-related datasets

A tip when working with analyst-related datasets is that they often contain vector data fields. One can extract different information from the same data field using different vector operators. Let's take anl16_estimate_d0_estvalue, for example, which provides information about the estimate value for each stock. Apart from the usual vec_avg, one can use the following operators:

+ vec_count(anl16_estimate_d0_estvalue) represents the number of analysts that provide an estimate for that stock. This can be used to filter out stocks with a low number of analysts, which might introduce noise during specific periods.

+ vec_stddev(anl16_estimate_d0_estvalue) or vec_range(anl16_estimate_d0_estvalue) can be used to measure how "spread out" the estimates are. The lower the spread, the higher the consensus.

[[1]](https://support.worldquantbrain.com#_ftnref1) Delay-0 Alphas are also referred to as D0 Alphas throughout.

[[2]](https://support.worldquantbrain.com#_ftnref2) WorldQuant defines “Alphas” as mathematical models that seek to predict the future price movements of various financial instruments.
