# Getting started with Model Datasets


Source: https://support.worldquantbrain.com/hc/en-us/community/posts/25238147759383-Getting-started-with-Model-Datasets


Tips for getting started with [Model](https://platform.worldquantbrain.com/data/data-sets?category=model) Datasets:

- Model datasets have well-structured data fields that are mostly scores. You can use common time series operations like rank, z-score, or measuring the delta of the fields.

- Measuring the time series correlation as well as co-skewness can yield good signals for model data fields. For this, use the 'ts_corr' and 'ts_co_skewness' operators.

- General guidance for using the group operators on model data fields is to try the following: 'group_rank', 'group_neutralize', 'group_normalize' and 'group_zscore'.

- Neutralizations depend on the category of the model being used. For example, [SmartRatios Model](https://platform.worldquantbrain.com/data/data-sets/model36) give scores for different metrics related to the credit worthiness of a particular company which can vary across sectors and industries. Therefore, sector and industry neutralizations are preferred for these.

- Since model datasets may be direct or indirect predictors of returns, you can take the correlation of data fields with close price or returns to judge its potential predictive power and create Alphas.

Example Alphas:

- Example Alpha Idea 1:
Fields based on Earnings Surprise, Earnings Growth, Cash Flow etc. tend to be highly predictive indicators of future returns. Time series analysis using 'ts_rank' or 'ts_zscore' should help in developing good Alphas. Similar to other model datasets, these data are also structured, and instead of raw values, you get scores in some form.
In some cases, analyzing these scores across large time periods can give insights about the trend of these scores, which can then be useful to write good Alphas.
In general, it is a good idea to compare these scores across smaller groups like industry or subindustry. You can use group operators like 'group_rank' or 'group_zscore' to do this.
Country and sector neutralizations generally work well, though we recommend you to try other groups as well
Since some fields of model datasets can be direct/indirect predictors of returns, you can take correlation of it with returns/close to assess its potential predictive power.

- Fields based on Earnings Surprise, Earnings Growth, Cash Flow etc. tend to be highly predictive indicators of future returns. Time series analysis using 'ts_rank' or 'ts_zscore' should help in developing good Alphas. Similar to other model datasets, these data are also structured, and instead of raw values, you get scores in some form.

- In some cases, analyzing these scores across large time periods can give insights about the trend of these scores, which can then be useful to write good Alphas.

- In general, it is a good idea to compare these scores across smaller groups like industry or subindustry. You can use group operators like 'group_rank' or 'group_zscore' to do this.

- Country and sector neutralizations generally work well, though we recommend you to try other groups as well

- Since some fields of model datasets can be direct/indirect predictors of returns, you can take correlation of it with returns/close to assess its potential predictive power.

- Example Alpha Idea 2:
EPS Estimate Model dataset gives EPS estimate value predicted by analysts. Time-series operators like 'ts_delta', 'ts_rank', 'ts_zscore' and 'ts_returns' can be helpful to measure the changes of the estimates and predict the stock price moving direction.
Using the surprise percentage fields of EPS Estimate Model dataset rather than estimate value directly can be more useful to compare companies of different sizes.
Scoring dataset has some well structured data fields such as scores, you can use common time series operations like 'rank', 'zscore' or measuring the delta of the fields.
Scoring dataset also provides some fields such as EPS growth forecast which are similar to EPS Estimate Model dataset. You can process those fields in the similar way.
Country and sector neutralizations generally work well, though we recommend you to try other groups as well.
Calculating estimate PE ratio using EPS estimates of either EPS Estimate Model dataset or Scoring dataset and price fields of basedata ([Price Volume Data for Equity](https://platform.worldquantbrain.com/data/data-sets/pv1)) PE ratio can be a good measurement to generate Alphas.

- EPS Estimate Model dataset gives EPS estimate value predicted by analysts. Time-series operators like 'ts_delta', 'ts_rank', 'ts_zscore' and 'ts_returns' can be helpful to measure the changes of the estimates and predict the stock price moving direction.

- Using the surprise percentage fields of EPS Estimate Model dataset rather than estimate value directly can be more useful to compare companies of different sizes.

- Scoring dataset has some well structured data fields such as scores, you can use common time series operations like 'rank', 'zscore' or measuring the delta of the fields.

- Scoring dataset also provides some fields such as EPS growth forecast which are similar to EPS Estimate Model dataset. You can process those fields in the similar way.

- Country and sector neutralizations generally work well, though we recommend you to try other groups as well.

- Calculating estimate PE ratio using EPS estimates of either EPS Estimate Model dataset or Scoring dataset and price fields of basedata ([Price Volume Data for Equity](https://platform.worldquantbrain.com/data/data-sets/pv1)) PE ratio can be a good measurement to generate Alphas.

Recommended Datasets:

- [Analysts' Factor Model](https://platform.worldquantbrain.com/data/data-sets/model77)

- [Fundamentals and Technical Indicators Model](https://platform.worldquantbrain.com/data/data-sets/model109)

- [Earnings Quality](https://platform.worldquantbrain.com/data/data-sets/model25)

- [EPS Estimate Model](https://platform.worldquantbrain.com/data/data-sets/model30)

- [Analyst Revisions Model Data](https://platform.worldquantbrain.com/data/data-sets/model216)
