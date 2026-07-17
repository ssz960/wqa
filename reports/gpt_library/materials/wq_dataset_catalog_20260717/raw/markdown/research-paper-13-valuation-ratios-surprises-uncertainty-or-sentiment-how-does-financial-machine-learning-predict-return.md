# Research Paper 13: Valuation Ratios, Surprises, Uncertainty or Sentiment: How Does Financial Machine Learning Predict Returns From Earnings Announcements?


Source: https://support.worldquantbrain.com/hc/en-us/community/posts/15465058281495-Research-Paper-13-Valuation-Ratios-Surprises-Uncertainty-or-Sentiment-How-Does-Financial-Machine-Learning-Predict-Returns-From-Earnings-Announcements


Abstract :

We apply state-of-the-art financial machine learning to assess the return-predictive value of more than 45,000 earnings announcements on a majority of S&P1500 constituents. To represent the diverse information content of earnings announcements, we generate predictor variables based on various sources such as analyst forecasts, earnings press releases and analyst conference call transcripts. We sort announcements into decile portfolios based on the models abnormal return prediction. In comparison to three benchmark models, we find that random forests yield superior abnormal returns which tend to increase with the forecast horizon for up to 60 days after the announcement. We subject the models learning and out-of-sample performance to further analysis. First, we find larger abnormal returns for small-cap stocks and a delayed return drift for growth stocks. Second, while revenue and earnings surprises are the main predictors for the contemporary reaction, we find that a larger range of variables, mostly fundamental ratios and forecast errors, is used to predict post-announcement returns. Third, we analyze variable contributions and find the model to recover non-linear patterns of common capital markets effects such as the value premium. Leveraging the models predictions in a zero-investment trading strategy yields annualized returns of 11.63 percent at a Sharpe ratio of 1.39 after transaction costs.

Authors: Yuyan Guan, Franco Wong, Yue Zhang

Year: 2015

Link : [https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3577132](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3577132)

Key ideas and Comments from WorldQuant:

- Page 14 Table 3

- Page 23 paragraph 2

The authors build a holistic view on earnings releases by combining various sources of information and build a few ML based alphas on SP1500. The paper includes a long list of features around earnings releases with sources and feature importance analysis.It can be a very immediate inspiration for earnings and sentiment alphas and a nice starting point for new researchers due to the large number of references.

Term

Data field

Dataset

customer

fnd6_custadv

[Company Fundamental Data for Equity](https://platform.worldquantbrain.com/data/data-sets/fundamental6)

earnings news

rp_css_earnings

[Ravenpack News Data](https://platform.worldquantbrain.com/data/data-sets/news18)

industry

industry

[Company Fundamental Data for Equity](https://platform.worldquantbrain.com/data/data-sets/fundamental6)
