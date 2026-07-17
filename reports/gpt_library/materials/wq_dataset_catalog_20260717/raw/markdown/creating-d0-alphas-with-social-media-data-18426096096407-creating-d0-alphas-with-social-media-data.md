# Creating D0 Alphas with Social Media Data


Source: https://support.worldquantbrain.com/hc/en-us/community/posts/18426096096407-Creating-D0-Alphas-with-Social-Media-Data


Introduction

In the rapidly evolving financial landscape, data from social media platforms has emerged as a unique and powerful resource for participants. Social media platforms provide real-time sentiment data, enabling participants seeking to track market trends, anticipate price movements, and make informed decisions. This document delves into the application of social media data in Late-Informed News Participation, a Delay-0[[1]](https://support.worldquantbrain.com#_ftn1) Alpha[[2]](https://support.worldquantbrain.com#_ftn2) tactic.

[[1]](https://support.worldquantbrain.com#_ftnref1) Delay-0 Alphas are also referred to as D0 Alphas throughout this document.

[[2]](https://support.worldquantbrain.com#_ftnref2) WorldQuant defines “Alphas” as mathematical models that seek to predict the future price movements of various financial instruments.

Late-Informed News Participation

Late-Informed News Participation is a tactic that seeks to capitalize on the price movements of financial instruments (stocks, commodities, currencies, etc.) based on the late arrival of significant news or information near the market close. The tactic is based on the intraday momentum model, positing that price movements tend to continue in the same direction within a single trading day. Key characteristics of this tactic include timing (identifying and exploiting late-arriving news close to the market close), news sentiment (incorporating both the content and sentiment of the news), and notably, social media sentiment.

An effective way to earn from Late-Informed News Participation involves developing a tactic idea that incorporates news sentiment data, social media sentiment data, and analyst ratings to identify potential opportunities. For example, a tactic idea could be generated based on the historical negativity scores from research reports. The underlying assumption in this example would be that the lower the negativity score, the more positive the sentiment in the research reports, indicating a bullish outlook for the asset.

Recommended/Relevant Datasets

- [Archive News Data (news104):](https://platform.worldquantbrain.com/data/data-sets/news104) News streaming and archive data for various sources and an aggregated feed of global press releases and exchange disclosure wires.

- [Sentiment Data by NLP (sentiment33):](https://platform.worldquantbrain.com/data/data-sets/sentiment33) Financial texts processed internally with sentiment produced for each document. Multiple sentiment models used. Positivity, negativity and neutrality/objectivity scores are provided along with other methods.

- [Sentiment Data for Equity (socialmedia12):](https://platform.worldquantbrain.com/data/data-sets/socialmedia12) This dataset provides sentiment data with different sentiment and volume. It analyses social media, news and opinions for financial markets to determine market mood and provides potential signals. It monitors thousands of sources in real time to output reliable trading signals.

- [Ravenpack News Data (news18):](https://platform.worldquantbrain.com/data/data-sets/news18) This dataset provides news sentiment and other financial indicators. It has a number of different indicators derived from news events relating to different categories and specific companies. Each news event is classified to reflect its sentiment, uniqueness, relevance to the underlying company and a few other parameters.

- [Webpage Views Data (sentiment7):](https://platform.worldquantbrain.com/data/data-sets/sentiment7) This dataset provides the daily volumes of views for the Wikipedia pages of the companies globally. The asset prices are a result of participation decisions of many individuals in the market. To make such decisions, people gather information; the wiki pages of companies provide a lot of information which people can refer to. The idea here is to see the relationship between the traffic views  on the wiki pages for companies and their asset prices.

- [Real Time News Feed Data (news7):](https://platform.worldquantbrain.com/data/data-sets/news7) Combines various text news feeds from multiple sources to provide useful data points to capture stock selection signals.

- [Dow Jones News Analytics Data (news3):](https://platform.worldquantbrain.com/data/data-sets/news3) The Sentiment Analysis Engine (SAE) is a software for producing sentiment indices that gauge different emotions of the public towards financial assets traded in exchange markets worldwide. Specific emotions about an asset are detected in texts by matching words of text with keywords from an emotional dictionary.

- [Web Sources News Sentiment Data (news20):](https://platform.worldquantbrain.com/data/data-sets/news20) This dataset provides real-time structured sentiment, relevance and novelty data for companies based on aggregated news from various sources.

- [sentiment32 - China Social Media Sentiment Data:](https://platform.worldquantbrain.com/data/data-sets/sentiment32) This dataset captures Chinese social media sentiment data, providing total counts of posts, positive/negative posts, etc. This could be particularly useful for participating in Chinese equities.

- [other547 - Alternative Analytics Data:](https://platform.worldquantbrain.com/data/data-sets/other547) This dataset provides analytics data for potential signals from a broad coverage of social media, news sites, and blogs. It could be useful for gauging wider market sentiment.

- [socialmedia12 - Sentiment Data for Equity:](https://platform.worldquantbrain.com/data/data-sets/socialmedia12)  This dataset provides sentiment data by analyzing social media, news, and opinions for financial markets to determine the market mood and provide related potential signals.

- [other74 - AI/ML Web Based Mention Data:](https://platform.worldquantbrain.com/data/data-sets/other74) This dataset contains the daily number of web-based mentions ("citations") of brand names owned by over 1,500 US listed corporations, providing another layer of market sentiment.

- [news46 - Relevant News Analytics Data:](https://platform.worldquantbrain.com/data/data-sets/news46) Though not strictly social media, this dataset includes rich structured information and potential signals on both scheduled and unscheduled news events. It continuously analyzes relevant information from major real-time newswires, online media, and trustworthy sources to produce real-time news analytics.

- [model261 - Factors Dislocations Data:](https://platform.worldquantbrain.com/data/data-sets/model261) This dataset provides risk factors data impacted during COVID-19, which could be used to gauge market sentiment during this period.

- [socialmedia4 - Brands and Social Media Data:](https://platform.worldquantbrain.com/data/data-sets/socialmedia4) This dataset looks into the presence of an asset on different social media platforms. It digs deeper to map assets to its different brands and their corresponding handles/pages on social media.

- [model130 - Retail Investor Data:](https://platform.worldquantbrain.com/data/data-sets/model130) This dataset quantifies retail participation using retail trading activity and information from social media forums.

- [news50 - Web News Analytics Data:](https://platform.worldquantbrain.com/data/data-sets/news50) This dataset allows for analysis of articles/news from leading publishers and web aggregators.

- [news36 - News Analytics Data:](http://news36/) This dataset analyzes and quantifies news with sentiment labels, event/topic categories, and classification confidence scores.

Alpha Example

Alpha Idea:

We generate a tactic idea based on the historical negativity scores from research reports. The underlying assumption is that the lower the negativity score, the more positive the sentiment in the research reports, which may be indicative of a bullish outlook for the asset.

Data Used:

oth429_research_reports_fundamental_keywords_4_method_3_filtered_neg. It records the sentiment score (with extra NLP filtering) and negativity score. Weighted average score for the entire document.

Implementation:

vec_avg(...): This function computes the average negativity score for each day.

ts_arg_min(..., 120): This function returns the relative index of the minimum value in the time series for the past 120 days. If the current day has the minimum value for the past 120 days, it returns 0. If the previous day has the minimum value for the past 120 days, it returns 1, and so on.

log(...): The formula takes the natural logarithm of the result from ts_arg_min. Applying the logarithm can help normalize the resulting value by reducing the effect of large outliers, making it easier to compare with other data.

The formula helps identify the relative index of the day with the lowest average negativity score over the past 120 days. This day might represent a turning point or a period when the market sentiment is at its most positive.

Alpha Expression:

log(ts_arg_min(vec_avg(oth429_research_reports_fundamental_keywords_4_method_3_filtered_neg), 120))

Performance:

Fitness_1.91_Sharpe_1.44, with settings on 'region': 'EUR', 'universe': 'TOP1200', 'delay': 0, 'decay': 3, 'neutralization': 'SUBINDUSTRY', 'truncation': 0.1, 'pasteurization': 'ON', 'unitHandling': 'VERIFY', 'nanHandling': 'ON'

Improvement Hint:

It's important to note that using this formula alone may not be sufficient to generate profitable tactic ideas. Additional factors should be considered, such as technical indicators, fundamental analysis, and risk management, in order to develop a more comprehensive and robust tactic.
