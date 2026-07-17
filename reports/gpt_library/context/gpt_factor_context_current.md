# GPT Factor Capability Context

## Use Boundary

The full CSV is a retrieval source, not a single prompt payload. GPT should first choose region / universe / delay / category, then retrieve a small field slice by dataset or semantic query.
Do not paste all 85,612 fields into one request. Use 10-80 candidate fields per factor-design turn, with descriptions only for the selected candidates.
Operators and settings are compact enough to provide as capability context; still filter operators by expression role and language.

## Field Registry

- Rows: 85612
- Datasets: 299
- Categories: 16
- SHA-256: F5CD01F3F4820E1753A6BF99029BA7A2FF30772813158BC12A1F5CF5DC99A102
- Scope: USA / TOP3000 / delay 1

### Field Types

- GROUP: 2041
- MATRIX: 67205
- SYMBOL: 8
- UNIVERSE: 7
- VECTOR: 16351

### Category Counts

- Analyst: 16981
- Earnings: 610
- Fundamental: 10921
- Imbalance: 2
- Insiders: 185
- Institutions: 86
- Macro: 36
- Model: 27788
- News: 2664
- Option: 619
- Other: 10330
- Price Volume: 12913
- Risk: 941
- Sentiment: 1207
- Short Interest: 110
- Social Media: 219

## Dataset Catalog

`dataset_id | dataset_name | category | field_count | field_types`
- `acquisition_model` | Corporate Acquisition Likelihood Model | Other | 15 | {'VECTOR': 15}
- `ai_equity_alpha` | AI Equity Alpha Forecasts | Model | 1108 | {'MATRIX': 293, 'VECTOR': 815}
- `ai_factor_transfer` | AI Enhanced Equity Factor Transfer | Model | 20 | {'MATRIX': 20}
- `ai_news_scores` | AI News Sentiment Scores | Other | 105 | {'MATRIX': 105}
- `analyst10` | Performance-Weighted Analyst Estimates | Analyst | 2258 | {'MATRIX': 1943, 'VECTOR': 315}
- `analyst11` | ESG scores | Analyst | 445 | {'MATRIX': 445}
- `analyst14` | Estimations of Key Fundamentals | Analyst | 868 | {'MATRIX': 857, 'VECTOR': 11}
- `analyst15` | Earnings forecasts | Analyst | 2567 | {'MATRIX': 2567}
- `analyst16` | Real Time Estimates | Analyst | 162 | {'MATRIX': 6, 'VECTOR': 156}
- `analyst2` | Analysts Estimates of Key Fundamentals | Analyst | 29 | {'MATRIX': 7, 'VECTOR': 22}
- `analyst21` | Indicators of Interest Data | Analyst | 16 | {'VECTOR': 16}
- `analyst34` | Dividend forecasts model | Analyst | 6 | {'VECTOR': 6}
- `analyst4` | Analyst Estimate Data for Equity | Analyst | 1324 | {'MATRIX': 1105, 'VECTOR': 219}
- `analyst44` | Integrated Broker Estimates | Analyst | 797 | {'MATRIX': 148, 'VECTOR': 649}
- `analyst45` | Analyst Trade Ideas | Analyst | 181 | {'VECTOR': 181}
- `analyst46` | Analyst Investment insight Data | Analyst | 6 | {'MATRIX': 6}
- `analyst49` | Analyst Estimation Data | Analyst | 324 | {'MATRIX': 254, 'VECTOR': 70}
- `analyst69` | Fundamental Analyst Estimates | Analyst | 646 | {'MATRIX': 310, 'VECTOR': 336}
- `analyst7` | Broker Estimates | Analyst | 1317 | {'MATRIX': 1317}
- `analyst82` | Analyst estimate prediction data | Analyst | 488 | {'MATRIX': 488}
- `analyst83` | Smart Conference call transcript data | Analyst | 383 | {'VECTOR': 383}
- `analyst92` | Linear, nonlinear, and region-specific models | Analyst | 17 | {'VECTOR': 17}
- `analyst_base_ref` | Analyst Estimates Base Reference | Analyst | 28 | {'MATRIX': 6, 'VECTOR': 22}
- `analyst_chart_cnn` | Deep Learning Analyst Chart Signals | Model | 367 | {'MATRIX': 367}
- `analyst_consensus` | Standardized Analyst Consensus Forecasts | Analyst | 3424 | {'MATRIX': 30, 'VECTOR': 3394}
- `analyst_earnings_ibes` | Global Analyst Earnings Forecasts | Model | 42 | {'MATRIX': 42}
- `analyst_factor_signals` | Global Analyst Factor Signals | Analyst | 922 | {'MATRIX': 922}
- `analyst_revision_horizons` | Multi Horizon Analyst Revision Signals | Model | 1095 | {'MATRIX': 1095}
- `behavioral_signals` | Behavioral Finance Signal Factors | Model | 7 | {'VECTOR': 7}
- `biasfree_analyst` | Bias Adjusted Analyst Forecasts | Analyst | 54 | {'MATRIX': 45, 'VECTOR': 9}
- `board_gov_stats` | US Board Governance and Leadership Metrics | Insiders | 46 | {'MATRIX': 46}
- `board_network` | Board Member Network Analysis | Model | 17 | {'MATRIX': 17}
- `chart_cnn_alpha` | Deep Learning Chart-Based Alpha | Model | 403 | {'MATRIX': 403}
- `chart_model_alpha` | Deep Learning Chart Returns Predictor | Price Volume | 281 | {'MATRIX': 281}
- `chart_return_model` | Deep Learning Chart Return Prediction | Price Volume | 248 | {'MATRIX': 248}
- `continuation_score` | Price Chart Continuation Pattern Similarity | Price Volume | 560 | {'MATRIX': 560}
- `cre_exposure_model` | Commercial Real Estate Exposure Model | Other | 2 | {'VECTOR': 2}
- `creator_signal_perf` | Finance Creator Prediction Performance | Social Media | 102 | {'VECTOR': 102}
- `dl_riskfree_returns` | Deep Learning Risk Free Returns | Other | 285 | {'MATRIX': 285}
- `dl_volume_pred` | Deep Learning Volume Prediction | Price Volume | 8 | {'MATRIX': 8}
- `earnings2` | Financial Event Calendar Data | Earnings | 12 | {'MATRIX': 12}
- `earnings27` | Earnings Update Emails Data | Earnings | 14 | {'VECTOR': 14}
- `earnings3` | Earnings Date Data | Earnings | 5 | {'MATRIX': 4, 'VECTOR': 1}
- `earnings4` | Effect of earnings announcement model | Earnings | 375 | {'MATRIX': 250, 'VECTOR': 125}
- `earnings5` | Earnings Date Breaks | Earnings | 5 | {'VECTOR': 5}
- `earnings6` | International Findings Data | Earnings | 52 | {'VECTOR': 52}
- `earnings7` | Horizon Earnings and Calendar North America | Earnings | 40 | {'VECTOR': 40}
- `earnings_chart_dl` | Deep Learning Earnings Chart Predictions | Earnings | 100 | {'MATRIX': 100}
- `earnings_risk` | Earnings Event Risk Model | Other | 9 | {'VECTOR': 9}
- `earnings_sent_matrix` | Global Earnings Call Sentiment Matrix | Earnings | 7 | {'MATRIX': 7}
- `earningscall_embed` | Earnings Call Text Embedding Analytics | Other | 515 | {'MATRIX': 515}
- `earningscall_sentiment` | Multi Aspect Earnings Call Sentiment | Other | 226 | {'MATRIX': 180, 'VECTOR': 46}
- `equity_forum_data` | International Equity Forum Activity | Other | 8 | {'VECTOR': 8}
- `equity_kpi_forecast` | US Equity KPI Forecasts | Other | 22 | {'VECTOR': 22}
- `event_relation` | Text-Based Event Relationship Analysis | Other | 9 | {'VECTOR': 9}
- `event_return_model` | Deep Learning Event Return Prediction | News | 59 | {'MATRIX': 59}
- `event_sentiment_signals` | Corporate Event Sentiment Signals | Other | 26 | {'VECTOR': 26}
- `event_stock_model` | Corporate Event Driven Stock Model | Model | 6 | {'VECTOR': 6}
- `expected_move` | Equity Expected Move Metrics | Model | 110 | {'MATRIX': 110}
- `filing_sentiment` | Regulatory Filing Sentiment Analytics | Other | 21 | {'VECTOR': 21}
- `finnews_nlp_scores` | Transformer Based Financial News Scores | Other | 105 | {'MATRIX': 105}
- `forum_sentiment` | Global Stock Forum Sentiment Signals | Other | 13 | {'VECTOR': 13}
- `forward_beta_risk` | Forward Beta Risk Prediction Model | Model | 42 | {'MATRIX': 28, 'VECTOR': 14}
- `fund_holdings_panel` | Global Institutional Fund Holdings | Institutions | 30 | {'VECTOR': 30}
- `fundamental1` | Management and Executive Data | Fundamental | 205 | {'VECTOR': 205}
- `fundamental110` | Press Release Data | Fundamental | 26 | {'VECTOR': 26}
- `fundamental13` | Comprehensive Fundamentals Dataset | Fundamental | 87 | {'MATRIX': 87}
- `fundamental14` | Audit Analytics Directors Data | Fundamental | 248 | {'VECTOR': 248}
- `fundamental17` | Direct Fundamental Data | Fundamental | 402 | {'MATRIX': 402}
- `fundamental2` | Report Footnotes | Fundamental | 766 | {'MATRIX': 766}
- `fundamental22` | Environmental and Social Governance Data | Fundamental | 14 | {'VECTOR': 14}
- `fundamental23` | Fundamental Point in Time Data | Fundamental | 1637 | {'MATRIX': 1610, 'VECTOR': 27}
- `fundamental25` | Company Operating Metrics | Fundamental | 8 | {'VECTOR': 8}
- `fundamental28` | Global Fundamental Data | Fundamental | 2209 | {'MATRIX': 2209}
- `fundamental3` | Fundamentals Data for US Equities | Fundamental | 788 | {'MATRIX': 784, 'VECTOR': 4}
- `fundamental31` | Additional Factor Model | Fundamental | 189 | {'MATRIX': 189}
- `fundamental44` | Accounting Quality Models | Fundamental | 11 | {'MATRIX': 11}
- `fundamental6` | Company Fundamental Data for Equity | Fundamental | 886 | {'MATRIX': 574, 'VECTOR': 312}
- `fundamental65` | Factor Ratios and its Rank Model | Model | 1155 | {'MATRIX': 1155}
- `fundamental69` | Quarterly Fundamental Data | Fundamental | 12 | {'MATRIX': 12}
- `fundamental7` | Comprehensive Fundamentals Data | Fundamental | 311 | {'MATRIX': 149, 'VECTOR': 162}
- `fundamental72` | Comprehensive Fundamental Data | Fundamental | 1852 | {'MATRIX': 730, 'VECTOR': 1122}
- `fundamental76` | Standardized Fundamental SEC Data | Fundamental | 128 | {'VECTOR': 128}
- `fundamental92` | Quantify text part in financial reports data | Fundamental | 3 | {'VECTOR': 3}
- `fundamental94` | Aggregated Fundamental Data | Fundamental | 571 | {'MATRIX': 571}
- `global_seasonal_model` | Global Seasonal Regime Return Signals | Model | 366 | {'MATRIX': 366}
- `hiring_trends` | Global Corporate Hiring Trends | Other | 3 | {'VECTOR': 3}
- `imbalance5` | Oil Price Resilience Scores | Imbalance | 2 | {'MATRIX': 2}
- `insider_agg_matrix` | Smart Insider Transaction Aggregates | Insiders | 17 | {'MATRIX': 17}
- `insider_feats` | Global Insider Transaction Features | Other | 118 | {'VECTOR': 118}
- `insider_matrix` | Aggregated Insider Transaction Matrix | Other | 33 | {'MATRIX': 33}
- `insider_trx_matrix` | Global Insider Transaction Aggregates | Other | 29 | {'MATRIX': 29}
- `insiders1` | Global Insider Trading Data | Insiders | 45 | {'MATRIX': 26, 'VECTOR': 19}
- `insiders3` | SEC Report Data | Insiders | 61 | {'MATRIX': 28, 'VECTOR': 33}
- `insiders4` | Edgar forms data | Insiders | 16 | {'MATRIX': 1, 'VECTOR': 15}
- `institutions18` | Ownership Model Data | Institutions | 17 | {'MATRIX': 15, 'VECTOR': 2}
- `institutions20` | Short Sale Volume Data | Institutions | 17 | {'MATRIX': 17}
- `institutions6` | Institutions and Beneficial Stake Ownership | Institutions | 22 | {'MATRIX': 22}
- `intraday_pv_feats` | Daily Intraday Price Volume Features | Price Volume | 582 | {'MATRIX': 582}
- `macro63` | Index Reconstitution Data | Macro | 3 | {'MATRIX': 3}
- `mfm_model_output` | Multi Factor Model Universal Output | Risk | 117 | {'MATRIX': 117}
- `ml_factor_proj` | Machine Learning Factor Projections | Other | 1070 | {'MATRIX': 1070}
- `mmp_nlp_sentiment` | Multilingual NLP News Sentiment Signals | Other | 1650 | {'MATRIX': 1629, 'VECTOR': 21}
- `model10` | Research Indicators | Model | 1224 | {'GROUP': 1, 'MATRIX': 1223}
- `model109` | Fundamentals and Technical Indicators Model | Model | 544 | {'MATRIX': 271, 'VECTOR': 273}
- `model113` | ML/AI-Estimates for Research Indicators | Model | 48 | {'MATRIX': 48}
- `model12` | Stock Selection Model | Model | 5 | {'MATRIX': 5}
- `model127` | Corporate Patent Innovation Activity Dataset | Model | 14 | {'VECTOR': 14}
- `model135` | Alternative technical factor models | Model | 273 | {'VECTOR': 273}
- `model138` | Stock Selection from Accounting-based Factors | Model | 120 | {'VECTOR': 120}
- `model139` | Inflation based stock selection model | Model | 4 | {'VECTOR': 4}
- `model140` | Sensitivity to the Inflation Change | Model | 3 | {'MATRIX': 3}
- `model141` | Interest Rate Sensitivity Measures | Model | 11 | {'MATRIX': 11}
- `model144` | Stock Selection DL model | Model | 2 | {'MATRIX': 2}
- `model16` | Fundamental Scores | Model | 24 | {'MATRIX': 24}
- `model165` | Time-series prediction of alpha models | Model | 441 | {'MATRIX': 441}
- `model17` | Research Analyst Estimate Factors | Model | 43 | {'MATRIX': 43}
- `model176` | Non-Financial Metric Models | Model | 84 | {'VECTOR': 84}
- `model211` | Analyst estimate prediction data | Analyst | 488 | {'MATRIX': 488}
- `model219` | Canadian Equity Quantitative Models | Model | 1282 | {'MATRIX': 1282}
- `model227` | Generalized Feature Transformer Dataset | Model | 173 | {'MATRIX': 173}
- `model23` | Scorings Data | Model | 157 | {'MATRIX': 157}
- `model230` | Factor Ratios and its Rank Model | Model | 1168 | {'MATRIX': 1168}
- `model237` | ETF Risk Data | Model | 234 | {'VECTOR': 234}
- `model240` | Qualitative Alpha Model Data | Model | 105 | {'VECTOR': 105}
- `model243` | Combined Alpha Model | Model | 4 | {'VECTOR': 4}
- `model25` | Earnings Quality | Model | 430 | {'MATRIX': 430}
- `model252` | Systematic Hedging for Investors to Evade Large Drawdowns | Model | 3 | {'VECTOR': 3}
- `model259` | Accounting governance indicator models | Model | 2 | {'MATRIX': 2}
- `model26` | Analyst Revisions | Model | 839 | {'MATRIX': 839}
- `model262` | DNN prediction of fundamentals | Model | 1208 | {'MATRIX': 1208}
- `model264` | Predictive data using Deep Learning models | Model | 2083 | {'MATRIX': 2083}
- `model267` | 8-K based NLP model | Model | 140 | {'MATRIX': 140}
- `model27` | Credit Risk Model | Model | 20 | {'MATRIX': 20}
- `model28` | Structural Credit Risk Model | Model | 104 | {'MATRIX': 104}
- `model30` | EPS Estimate Model | Model | 48 | {'MATRIX': 44, 'SYMBOL': 4}
- `model307` | Global Sales Allocation Model Data | Model | 15 | {'VECTOR': 15}
- `model31` | Earnings Quality Model | Model | 235 | {'MATRIX': 235}
- `model313` | Intangible Asset Factors | Model | 13 | {'MATRIX': 13}
- `model354` | Comprehensive Factor Analytics Data | Model | 310 | {'VECTOR': 310}
- `model36` | SmartRatios Model | Model | 32 | {'MATRIX': 32}
- `model37` | Text Mining Data | Model | 95 | {'MATRIX': 95}
- `model39` | Valuation Momentum Data | Model | 40 | {'MATRIX': 40}
- `model51` | Systematic Risk Metrics | Model | 16 | {'MATRIX': 16}
- `model53` | Creditworthiness Risk Measure Model | Model | 138 | {'MATRIX': 116, 'VECTOR': 22}
- `model59` | Credit Analytics Data | Model | 1 | {'VECTOR': 1}
- `model68` | Risk-Alleviated Momentum Scores | Model | 12 | {'VECTOR': 12}
- `model77` | Analysts' Factor Model | Model | 3256 | {'MATRIX': 3256}
- `multi_horizon_alpha` | Multi Horizon Alpha Decomposition | Model | 832 | {'MATRIX': 832}
- `multi_source_model` | Multi-Source Market Return Prediction | Model | 62 | {'MATRIX': 62}
- `multifactor_return_pred` | Multi Factor Market Return Predictions | Model | 669 | {'MATRIX': 669}
- `news104` | Archive News Data | News | 32 | {'VECTOR': 32}
- `news12` | US News Data | News | 875 | {'MATRIX': 75, 'VECTOR': 800}
- `news17` | PR Edition Data | News | 45 | {'VECTOR': 45}
- `news18` | Ravenpack News Data | News | 121 | {'MATRIX': 71, 'VECTOR': 50}
- `news21` | Macro Economic Event Data | News | 260 | {'MATRIX': 43, 'VECTOR': 217}
- `news23` | MnA Deals Data | News | 129 | {'VECTOR': 129}
- `news29` | Significant Developments Data | News | 12 | {'VECTOR': 12}
- `news3` | Dow Jones News Analytics Data | News | 19 | {'VECTOR': 19}
- `news31` | News Analytics on Equities | News | 60 | {'VECTOR': 60}
- `news36` | News Analytics Data | News | 29 | {'VECTOR': 29}
- `news38` | News Analytic Model Data | News | 63 | {'VECTOR': 63}
- `news42` | US/AMR news data | News | 9 | {'VECTOR': 9}
- `news46` | Relevant News Analytics Data | News | 91 | {'MATRIX': 33, 'VECTOR': 58}
- `news48` | Global Media News Data | News | 22 | {'VECTOR': 22}
- `news5` | News Feed Analytics Data | News | 145 | {'VECTOR': 145}
- `news50` | Web News Analytics Data | News | 83 | {'MATRIX': 21, 'VECTOR': 62}
- `news51` | Aggregated News Data | News | 15 | {'VECTOR': 15}
- `news52` | Conference call data | News | 42 | {'MATRIX': 36, 'VECTOR': 6}
- `news55` | Intermediate News Data | News | 6 | {'VECTOR': 6}
- `news59` | Corporate Events Data | News | 71 | {'MATRIX': 67, 'VECTOR': 4}
- `news7` | Real Time News Feed Data | News | 162 | {'MATRIX': 67, 'VECTOR': 95}
- `news73` | Story by Story Sentiment | News | 22 | {'VECTOR': 22}
- `news76` | Textual News Feed Data | News | 6 | {'VECTOR': 6}
- `news82` | Sentiment Analysis from DNN | News | 23 | {'MATRIX': 20, 'VECTOR': 3}
- `news84` | Headline Sentiment Analysis using DNN | News | 23 | {'MATRIX': 20, 'VECTOR': 3}
- `news85` | News Sentiment Analysis using DNN | News | 23 | {'MATRIX': 20, 'VECTOR': 3}
- `news87` | Smart Conference call transcript data | Analyst | 214 | {'VECTOR': 214}
- `news92` | Standardized Financial News Categorization | News | 48 | {'VECTOR': 48}
- `news94` | Intraday Post News Price Volume | News | 54 | {'VECTOR': 54}
- `news97` | Web News Sentiment Scores | News | 105 | {'MATRIX': 105}
- `news_sentiment_dl` | Deep Learning News Sentiment Signals | Other | 88 | {'VECTOR': 88}
- `news_sentiment_nlp` | News Sentiment Signal Features | Other | 23 | {'VECTOR': 23}
- `news_sentiment_transfer` | Transferred News Sentiment Analytics | Sentiment | 23 | {'MATRIX': 20, 'VECTOR': 3}
- `news_transformer_scores` | Transformer Based News Sentiment Scores | Sentiment | 315 | {'MATRIX': 315}
- `nlp_news_scores` | Transformer-Based News Sentiment Analytics | Other | 84 | {'MATRIX': 84}
- `option3` | Equity Options Moneyness Aggregates | Option | 20 | {'MATRIX': 20}
- `option40` | Options Analytics Data | Option | 208 | {'MATRIX': 208}
- `option6` | Forecasted Volatility for Equity Options | Option | 133 | {'MATRIX': 133}
- `option8` | Volatility Data | Option | 64 | {'MATRIX': 64}
- `option9` | Options Analytics | Option | 74 | {'MATRIX': 74}
- `option_chart_model` | Option Chart Image Return Prediction | Model | 439 | {'MATRIX': 439}
- `option_horizon_decomp` | US Equity Option Horizon Decomposition | Model | 501 | {'MATRIX': 501}
- `options_composite` | Options Derived Composite Signals | Model | 143 | {'MATRIX': 84, 'VECTOR': 59}
- `order_book_imbalance` | Order Book Liquidity and Imbalance Analytics | Other | 198 | {'VECTOR': 198}
- `order_flow_imb` | Institutional Order Flow Imbalance | Option | 120 | {'MATRIX': 120}
- `other128` | Global Executive Performance Factors | Other | 12 | {'VECTOR': 12}
- `other143` | Transaction Volume Data for Equity | Other | 126 | {'MATRIX': 105, 'VECTOR': 21}
- `other17` | Flow into Equities Data | Other | 4 | {'MATRIX': 4}
- `other176` | Nonlinear adaptive model | Model | 20 | {'MATRIX': 20}
- `other193` | Systematic Hedging for Investors to Evade Large Drawdowns | Model | 3 | {'VECTOR': 3}
- `other250` | details data | Other | 10 | {'VECTOR': 10}
- `other296` | Corporate Earnings Call Sentiment Data | Other | 47 | {'VECTOR': 47}
- `other315` | Equity Swap Data | Other | 32 | {'VECTOR': 32}
- `other326` | Intermediate Data from Events | Other | 53 | {'MATRIX': 17, 'VECTOR': 36}
- `other327` | Sensitivity to Interest Rates Model | Other | 3 | {'MATRIX': 3}
- `other33` | Qualitative Alpha Model Data | Model | 51 | {'VECTOR': 51}
- `other335` | Multi-Region Dividend Alpha Model Dataset | Other | 10 | {'MATRIX': 10}
- `other359` | Web Comments & Reaction Data | Other | 10 | {'VECTOR': 10}
- `other378` | Accounting governance indicator models | Model | 2 | {'MATRIX': 2}
- `other384` | NLP on conference conversation | Other | 66 | {'VECTOR': 66}
- `other411` | Linear, nonlinear, and region-specific models | Analyst | 17 | {'VECTOR': 17}
- `other424` | Dividend prediction model | Other | 3 | {'MATRIX': 3}
- `other427` | Quantify text part in financial reports data | Fundamental | 3 | {'VECTOR': 3}
- `other432` | DNN prediction of fundamentals | Model | 1139 | {'MATRIX': 1139}
- `other436` | Dividend model | Other | 3 | {'VECTOR': 3}
- `other455` | Relationship enhanced with AI/ML | Other | 1425 | {'GROUP': 1200, 'MATRIX': 225}
- `other460` | Predictive data using Deep Learning models | Model | 2038 | {'MATRIX': 2038}
- `other466` | Aggregated Fundamental Data | Fundamental | 565 | {'MATRIX': 565}
- `other510` | 8-K based NLP model | Model | 10 | {'MATRIX': 10}
- `other545` | Linked Firms Momentum Data | Other | 4 | {'VECTOR': 4}
- `other546` | Institutional Network Analysis Dataset | Other | 13 | {'VECTOR': 13}
- `other551` | Alpha Toolkit Dataset | Macro | 33 | {'MATRIX': 33}
- `other553` | Financial Opinion Mining | Sentiment | 74 | {'MATRIX': 33, 'VECTOR': 41}
- `other566` | Image-Based Financial Prediction Dataset | Other | 51 | {'MATRIX': 51}
- `other567` | Employee Review Data | Other | 223 | {'VECTOR': 223}
- `other571` | Wikipedia Viewing Data | Other | 30 | {'MATRIX': 30}
- `other580` | Standardized Daily ETF Holdings | Other | 403 | {'MATRIX': 403}
- `other596` | Sentiment Scores Data | Other | 420 | {'MATRIX': 420}
- `other623` | Text Blob News data | Other | 6 | {'VECTOR': 6}
- `other635` | Thomson Reuters News Analytics Equities | Other | 9 | {'VECTOR': 9}
- `other685` | Enhanced Financial Indicators | Other | 72 | {'MATRIX': 72}
- `other696` | Hybrid NLP Model | Other | 498 | {'VECTOR': 498}
- `other699` | Individual Investor Transactions Data | Other | 19 | {'VECTOR': 19}
- `other7` | Archive News Data | News | 10 | {'VECTOR': 10}
- `pattern_scores` | Chart Pattern Similarity Scores | Price Volume | 504 | {'MATRIX': 504}
- `predictive_starmine` | Predictive Analyst-Company Signal Set | Model | 1196 | {'MATRIX': 1196}
- `price_signal_dl` | Deep Learning Price Signal Dataset | Model | 28 | {'MATRIX': 28}
- `pv1` | Price Volume Data for Equity | Price Volume | 24 | {'GROUP': 7, 'MATRIX': 13, 'SYMBOL': 4}
- `pv103` | Interval and MOO&MOC statistics | Price Volume | 79 | {'MATRIX': 79}
- `pv104` | Market Microstructure Data | Price Volume | 46 | {'MATRIX': 46}
- `pv106` | Microstructure Spread Data | Price Volume | 6 | {'MATRIX': 6}
- `pv109` | Bond Yield Data | Price Volume | 34 | {'VECTOR': 34}
- `pv115` | Trading Data | Price Volume | 12 | {'MATRIX': 12}
- `pv13` | Relationship Data for Equity | Price Volume | 165 | {'GROUP': 135, 'MATRIX': 30}
- `pv141` | VWAP Tick Data | Price Volume | 6 | {'MATRIX': 4, 'VECTOR': 2}
- `pv149` | Holidays and Trading Hours Calendar | Price Volume | 6 | {'MATRIX': 6}
- `pv173` | Corporate Bond Pricing Data | Price Volume | 51 | {'VECTOR': 51}
- `pv20` | Daily Spot and Cross Rate Data | Price Volume | 1552 | {'GROUP': 14, 'MATRIX': 1498, 'VECTOR': 40}
- `pv29` | Derived Industry Classification | Price Volume | 199 | {'GROUP': 24, 'MATRIX': 175}
- `pv30` | Alternate Industry Classification | Price Volume | 833 | {'GROUP': 660, 'MATRIX': 173}
- `pv47` | Specific Return Dataset | Price Volume | 2 | {'MATRIX': 2}
- `pv48` | US Market Index Data | Price Volume | 147 | {'MATRIX': 102, 'VECTOR': 45}
- `pv52` | Order Excecution Summary | Price Volume | 176 | {'VECTOR': 176}
- `pv53` | Index Market Data | Price Volume | 5 | {'MATRIX': 5}
- `pv63` | Order Book Dataset | Price Volume | 16 | {'MATRIX': 16}
- `pv64` | Fund Holding Data | Price Volume | 245 | {'VECTOR': 245}
- `pv73` | Custom Relationship Data | Price Volume | 69 | {'VECTOR': 69}
- `pv87` | Aggregated dataset | Price Volume | 6666 | {'MATRIX': 6654, 'VECTOR': 12}
- `pv96` | Corporate Action Dataset | Price Volume | 32 | {'MATRIX': 23, 'VECTOR': 9}
- `pv98` | Intraday Tick Data and Statistics | Price Volume | 352 | {'MATRIX': 352}
- `pv_tech_indicators` | Price Volume Technical Indicators | Model | 56 | {'MATRIX': 56}
- `quant_factor_lib` | Multi-Domain Quantitative Factor Library | Model | 224 | {'VECTOR': 224}
- `risk59` | Securities Lending and Short Market Dynamics Dataset | Risk | 16 | {'VECTOR': 16}
- `risk60` | Securities Lending Insight Data | Risk | 5 | {'VECTOR': 5}
- `risk62` | Beta Risk Factors | Risk | 636 | {'MATRIX': 636}
- `risk65` | ETF Risk Model Data | Risk | 6 | {'MATRIX': 6}
- `risk70` | Multi-Factor Model | Risk | 158 | {'MATRIX': 158}
- `risk72` | Specific return of extended factors | Risk | 3 | {'MATRIX': 3}
- `risk82` | ETF Risk Data | Model | 234 | {'VECTOR': 234}
- `search_interest` | Rapid Search Interest Signals | Other | 11 | {'VECTOR': 11}
- `sentiment1` | Research Sentiment Data | Sentiment | 19 | {'MATRIX': 19}
- `sentiment21` | AI Sentiment Score Data | Sentiment | 258 | {'MATRIX': 258}
- `sentiment22` | News Sentiment Scores | Sentiment | 210 | {'MATRIX': 210}
- `sentiment23` | Textual Sentiment Analysis Data | Sentiment | 210 | {'MATRIX': 210}
- `sentiment26` | Website Popularity Ranking Dataset | Sentiment | 36 | {'VECTOR': 36}
- `sentiment27` | Website Popularity Rankings | Sentiment | 17 | {'VECTOR': 17}
- `sentiment7` | Webpage Views  Data | Sentiment | 45 | {'VECTOR': 45}
- `short_interest_pred` | Short Interest Forecast Signals | Short Interest | 10 | {'MATRIX': 10}
- `shortinterest24` | Short Sale Circuit Breaker Data | Short Interest | 1 | {'MATRIX': 1}
- `shortinterest29` | Group Short Sale Data | Short Interest | 32 | {'MATRIX': 32}
- `shortinterest3` | Securities Lending Files Data | Short Interest | 31 | {'VECTOR': 31}
- `shortinterest43` | Short Sell Dataset | Short Interest | 32 | {'MATRIX': 32}
- `shortinterest7` | Short Selling Model | Model | 16 | {'VECTOR': 16}
- `social_sent_score` | Equity Social Sentiment Scores | Other | 3 | {'VECTOR': 3}
- `socialmedia12` | Sentiment Data for Equity | Social Media | 18 | {'MATRIX': 12, 'VECTOR': 6}
- `socialmedia8` | Social Media Data for Equity | Social Media | 4 | {'MATRIX': 4}
- `stock_cluster_dl` | Deep Learning Stock Clusters | Other | 4 | {'MATRIX': 4}
- `stock_search_trends` | US Stock Search Trend Matrix | Other | 12 | {'MATRIX': 12}
- `sustainable_profit` | Sustainable Profitability Factor Library | Other | 122 | {'VECTOR': 122}
- `tech_chart_model` | Technical Indicator Chart Prediction | Model | 384 | {'MATRIX': 384}
- `techindi_model` | Deep Learning Technical Indicator Returns | Other | 1830 | {'MATRIX': 1830}
- `twitter_sentiment_l2` | Twitter Sentiment Signal Aggregation | Social Media | 95 | {'MATRIX': 95}
- `univ1` | Universe Dataset | Price Volume | 6 | {'UNIVERSE': 6}
- `univ2` | Universe Dataset | Price Volume | 1 | {'UNIVERSE': 1}
- `us_equity_news` | US Equity Quantitative News Sentiment | Other | 8 | {'VECTOR': 8}
- `us_short_sale` | US Equity Short Sale Volume | Short Interest | 4 | {'MATRIX': 4}
- `web_traffic_engage` | Web Traffic Engagement Signals | Other | 105 | {'MATRIX': 105}
- `workforce_flow_skills` | Global Workforce Flow and Skills Analytics | Other | 26 | {'VECTOR': 26}

## Settings Capability

- decay (Decay): integer [0, 512]
- delay (Delay): instrumentType/EQUITY/region/USA=[1, 0]; instrumentType/EQUITY/region/GLB=[1]; instrumentType/EQUITY/region/EUR=[1, 0]; instrumentType/EQUITY/region/ASI=[1]; instrumentType/EQUITY/region/CHN=[0, 1]; instrumentType/EQUITY/region/JPN=[1, 0]; instrumentType/EQUITY/region/IND=[1]; instrumentType/EQUITY/region/MEA=[1]
- instrumentType (Instrument type): EQUITY
- language (Language): PYTHON, FASTEXPR
- lookback (Lookback): integer [0, 1024]
- maxPosition (Max position): OFF, ON
- maxTrade (Max trade): OFF, ON
- nanHandling (Nan handling): ON, OFF
- neutralization (Neutralization): instrumentType/EQUITY/region/USA=[NONE, REVERSION_AND_MOMENTUM, STATISTICAL, CROWDING, FAST, SLOW, MARKET, SECTOR, INDUSTRY, SUBINDUSTRY, SLOW_AND_FAST]; instrumentType/EQUITY/region/GLB=[NONE, REVERSION_AND_MOMENTUM, STATISTICAL, CROWDING, FAST, SLOW, MARKET, SECTOR, INDUSTRY, SUBINDUSTRY, COUNTRY, SLOW_AND_FAST]; instrumentType/EQUITY/region/EUR=[NONE, REVERSION_AND_MOMENTUM, STATISTICAL, CROWDING, FAST, SLOW, MARKET, SECTOR, INDUSTRY, SUBINDUSTRY, COUNTRY, SLOW_AND_FAST]; instrumentType/EQUITY/region/ASI=[NONE, REVERSION_AND_MOMENTUM, STATISTICAL, CROWDING, FAST, SLOW, MARKET, SECTOR, INDUSTRY, SUBINDUSTRY, COUNTRY, SLOW_AND_FAST]; instrumentType/EQUITY/region/CHN=[NONE, REVERSION_AND_MOMENTUM, STATISTICAL, CROWDING, FAST, SLOW, MARKET, SECTOR, INDUSTRY, SUBINDUSTRY, SLOW_AND_FAST]; instrumentType/EQUITY/region/JPN=[NONE, REVERSION_AND_MOMENTUM, STATISTICAL, CROWDING, FAST, SLOW, MARKET, SECTOR, INDUSTRY, SUBINDUSTRY, SLOW_AND_FAST]; instrumentType/EQUITY/region/IND=[NONE, REVERSION_AND_MOMENTUM, STATISTICAL, CROWDING, FAST, SLOW, MARKET, SECTOR, INDUSTRY, SUBINDUSTRY, SLOW_AND_FAST]; instrumentType/EQUITY/region/MEA=[NONE, MARKET, SECTOR, INDUSTRY, SUBINDUSTRY, COUNTRY]
- pasteurization (Pasteurization): ON, OFF
- region (Region): instrumentType/EQUITY=[USA, GLB, EUR, ASI, CHN, JPN, IND, MEA]
- selectionHandling (Selection handling): POSITIVE, NON_ZERO, NON_NAN
- selectionLimit (Selection limit): integer [10, 1000]
- testPeriod (Test period): string [P0Y0M0D, P6Y0M0D]
- truncation (Truncation): float [0, 1]
- unitHandling (Unit handling): VERIFY
- universe (Universe): instrumentType/EQUITY/region/USA=[TOP3000, TOP2000, TOP1000, TOP500, TOP200, ILLIQUID_MINVOL1M, TOPSP500]; instrumentType/EQUITY/region/GLB=[TOP3000, MINVOL1M, MINVOL10M, TOPDIV3000]; instrumentType/EQUITY/region/EUR=[TOP2500, TOP1200, TOP800, TOP400, ILLIQUID_MINVOL1M, TOPCS1600]; instrumentType/EQUITY/region/ASI=[MINVOL1M, MINVOL10M, ILLIQUID_MINVOL1M, TOP500]; instrumentType/EQUITY/region/CHN=[TOP2000U]; instrumentType/EQUITY/region/JPN=[TOP1600, TOP1200]; instrumentType/EQUITY/region/IND=[TOP500]; instrumentType/EQUITY/region/MEA=[TOP400, TOP300]
- visualization (Visualization): boolean

### Captured UI Default Profile

- Source: VISIBLE_BRAIN_UI_BASELINE_20260716
- instrumentType: EQUITY
- region: USA
- universe: TOP3000
- delay: 1
- neutralization: SUBINDUSTRY
- decay: 4
- truncation: 0.08
- pasteurization: ON
- unitHandling: VERIFY
- nanHandling: OFF
- testPeriod: P1Y0M0D
- maxTrade: OFF
- maxPosition: OFF

## Operators

- Count: 85

### Arithmetic

- `abs(x)`: Returns the absolute value of a number, removing any negative sign.
- `add(x, y, filter = false), x + y`: Adds two or more inputs element wise. Set filter=true to treat NaNs as 0 before summing.
- `densify(x)`: Converts a grouping field of many buckets into lesser number of only available buckets so as to make working with grouping fields computationally efficient
- `divide(x, y), x / y`: Returns x divided by y (x / y). Note: dividing by zero raises an error; to avoid it, use divide(x, add(y, 0.0001)); adding a small epsilon to the denominator prevents divide-by-zero errors.
- `inverse(x)`: Returns the reciprocal of x (1 / x). Note: errors when x = 0; to avoid it, use inverse(add(x, 0.0001)); adding a small epsilon prevents divide-by-zero errors.
- `log(x)`: Calculates the natural logarithm of the input value. Commonly used to transform data that has positive values.
- `max(x, y, ..)`: Maximum value of all inputs. At least 2 inputs are required
- `min(x, y ..)`: Minimum value of all inputs. At least 2 inputs are required
- `multiply(x ,y, ... , filter=false), x * y`: Multiplies two or more inputs element wise. Set filter=true to treat NaNs as 0 before multiplication
- `power(x, y)`: Returns x raised to the power of y (x ^ y). Note: power(x, y) can drop the sign of x when y is non-integer; use signed_power(x, y) to preserve the sign of x.
- `reverse(x)`:  - x
- `sigmoid(x)`: Returns 1 / (1 + exp(-x))
- `sign(x)`: Returns the sign of a number: +1 for positive, -1 for negative, and 0 for zero. If the input is NaN, returns NaN.

Input: Value of 7 instruments at day t: (2, -3, 5, 6, 3, NaN, -10)
Output: (1, -1, 1, 1, 1, NaN, -1)
- `signed_power(x, y)`: x raised to the power of y such that final result preserves sign of x
- `sqrt(x)`: Returns the non-negative square root of x. Equivalent to power(x, 0.5). Note: for x < 0 the result is undefined; to retain the sign of x, use signed_power(x, 0.5) instead.
- `subtract(x, y, filter=false), x - y`: Subtracts inputs left to right: x ? y ? … Supports two or more inputs. Set filter=true to treat NaNs as 0 before subtraction.
- `tanh(x)`: Hyperbolic tangent of x

### Cross Sectional

- `normalize(x, useStd = false, limit = 0.0)`: Centers a daily cross section by subtracting the market mean; optionally divide by the cross sectional standard deviation and clamp the result to [?limit, +limit]. NaNs are ignored in mean/std.
- `quantile(x, driver = gaussian, sigma = 1.0)`: Ranks and shifts a vector of Alpha values, then applies a chosen statistical distribution (gaussian, cauchy, or uniform) to reduce outliers. The sigma parameter controls the scale of the output.
- `rank(x, rate=2)`: Ranks the values of the input x among all instruments, returning numbers evenly spaced between 0.0 and 1.0. Useful for normalizing data and reducing the impact of outliers.
- `regression_proj(y, x)`: Conducts the cross-sectional regression on the stocks with Y as target and X as the independent variable
- `scale(x, scale=1, longscale=1, shortscale=1)`: Scales the input so that the sum of absolute values across all instruments equals a specified book size. Allows separate scaling for long and short positions using optional parameters.
- `vector_neut(x, y)`: For given vectors x and y, it finds a new vector x* (output) such that x* is orthogonal to y
- `vector_proj(x, y)`: Returns vector projection of x onto y.
- `winsorize(x, std=4)`: Winsorize limits values in a data to within a specified number of standard deviations from the mean, reducing the impact of extreme outliers. Note: recommended std values range from 2 to 5: std = 2, 3, 4, 5 removes approximately 4.5%, 0.27%, 0.01%, and 0.0001% of extreme values, respectively (higher std removes fewer extremes).
- `zscore(x)`: Z-score is a numerical measurement that describes a value's relationship to the mean of a group of values. Z-score is measured in terms of standard deviations from the mean

### Group

- `group_backfill(x, group, d, std = 4.0)`: Fills missing (NaN) values for instruments within the same group by calculating a winsorized mean of all non-NaN values over the past d days. The winsorized mean is computed by trimming extreme values based on a specified standard deviation multiplier (std, default 4.0).
- `group_cartesian_product(g1, g2)`: Merge two groups into one group. If originally there are len_1 and len_2 group indices in g1 and g2, there will be len_1 * len_2 indices in the new group.
- `group_extra(x, weight, group)`: Replaces NaN values by their corresponding group means.
- `group_mean(x, weight, group)`: Calculates the harmonic mean of a data field within each specified group.
- `group_neutralize(x, group)`: Neutralizes Alpha values within each specified group by subtracting the group mean from each value. Groups can be industry, sector, country, or any custom grouping.
- `group_rank(x, group)`: Ranks each element within its group based on the input field, assigning a value between 0.0 and 1.0. This helps compare items within the same group, such as stocks in the same industry.
- `group_scale(x, group)`: Normalizes values within each group to a range between 0 and 1, making data comparable across different groups.
- `group_zscore(x, group)`: Calculates the Z-score of each value within its group, showing how far each value is from the group mean in terms of standard deviations. Useful for comparing values relative to their group.

### Logical

- `and(input1, input2)`: Returns 1 ('true') if both inputs are 1 ('true'). Otherwise, returns 0 ('false').
- `input1 == input2`: Returns 1 ('true') if input1 and input2 are the same. Otherwise, returns 0 ('false').
- `input1 > input2`: Returns 1 ('true') if input1 is a larger than input2. Otherwise, returns 0 ('false').
- `input1 >= input2`: Returns 1 ('true') if input1 is a larger or the same as input2. Otherwise, returns 0 ('false').
- `if_else(input1, input2, input 3)`: The if_else operator returns one of two values based on a condition. If the condition is true, it returns the first value; if false, it returns the second value.
- `is_nan(input)`: If (input == NaN) return 1 else return 0
- `input1 < input2`: Returns 1 ('true') if input1 is a smaller than input2. Otherwise, returns 0 ('false').
- `input1 <= input2`: Returns 1 ('true') if input1 is a smaller or the same as input2. Otherwise, returns 0 ('false').
- `not(x)`: Returns the logical negation of x. Returns 0 when x is 1 (‘true’) and 1 when x is 0 (‘false’).
- `input1!= input2`: Returns 1 ('true') if input1 and input2 are different numbers. Otherwise, returns 0 ('false').
- `or(input1, input2)`: Returns 1 if either input is true (either input1 or input2 has a value of 1), otherwise it returns 0.

### Special

- `inst_pnl(x)`: Generate pnl per instruments. Please note that the use of the inst_pnl() operator in an Alpha Expression is considered as utilizing the pv1 dataset (Price Volume Data for Equity) since it relies on pv1 data for calculations.

### Time Series

- `days_from_last_change(x)`: Calculates the number of days since the last change in the value of a given variable.
- `hump(x, hump = 0.01)`: Limits amount and magnitude of changes in input (thus reducing turnover)
- `kth_element(x, d, k, ignore=“NaN”)`: Returns the K-th value from a time series by looking back over a specified number of (‘d’) days, with the option to ignore certain values. Commonly used for backfilling missing data.
- `last_diff_value(x, d)`: Returns the most recent value of x from the past d days that is different from the current value of x.
- `ts_arg_max(x, d)`: Returns the number of days since the maximum value occurred in the last d days of a time series. If today's value is the maximum, returns 0; if it was yesterday, returns 1, and so on.
- `ts_arg_min(x, d)`: Returns the number of days since the minimum value occurred in a time series over the past d days. If today's value is the minimum, returns 0; if it was yesterday, returns 1, and so on.
- `ts_av_diff(x, d)`: Calculates the difference between a value and its mean over a specified period, ignoring NaN values in the mean calculation. In short, it returns x – ts_mean(x, d) with NaNs ignored.
- `ts_backfill(x,lookback = d, k=1)`: Replaces missing (NaN) values in a time series with the most recent valid value from a specified lookback window, improving data coverage and reducing risk from missing data.
- `ts_corr(x, y, d)`: Calculates the Pearson correlation between two variables, x and y, over the past d days, showing how closely they move together.
- `ts_count_nans(x ,d)`: Counts the number of missing (NaN) values in a data series over a specified number of days.
- `ts_covariance(y, x, d)`: Calculates the covariance between two time-series variables, y and x, over the past d days. Useful for measuring how two variables move together within a specified historical window.
- `ts_decay_linear(x, d, dense = false)`: Applies a linear decay to time-series data over a set number of days, smoothing the data by averaging recent values and reducing the impact of older or missing data.
- `ts_delay(x, d)`: Returns the value of a variable x from d days ago. Use this operator to access historical data points by specifying the desired time lag in days.
- `ts_delta(x, d)`: Calculates the difference between a value and its delayed version over a specified period. Useful for measuring changes or momentum in time-series data.
- `ts_entropy(x,d)`: For each instrument, we collect values of input in the past d days and calculate the probability distribution then the information entropy via a histogram as a result
- `ts_mean(x, d)`: Calculates the simple average (mean) value of a variable x over the past d days.
- `ts_min_diff(x, d)`: Returns x - ts_min(x, d)
- `ts_min_max_cps(x, d, f = 2)`: Returns (ts_min(x, d) + ts_max(x, d)) - f * x. If not specified, by default f = 2
- `ts_min_max_diff(x, d, f = 0.5)`: Returns x - f * (ts_min(x, d) + ts_max(x, d)). If not specified, by default f = 0.5
- `ts_product(x, d)`: Returns the product of the values of x over the past d days. Useful for calculating geometric means and compounding returns or growth rates.
- `ts_quantile(x,d, driver="gaussian" )`: Calculates the ts_rank of the input and transforms it using the inverse cumulative distribution function (quantile function) of a specified probability distribution (default: Gaussian/normal). This helps to normalize or reshape the distribution of your data over a rolling window.
- `ts_rank(x, d, constant = 0)`: Ranks the value of a variable for each instrument over a specified number of past days, returning the rank of the current value (optionally adjusted by a constant). Useful for normalizing time-series data and highlighting relative performance over time.
- `ts_regression(y, x, d, lag = 0, rettype = 0)`: Returns various parameters related to regression function
- `ts_scale(x, d, constant = 0)`: Scales a time series to a 0–1 range based on its minimum and maximum values over a specified period, with an optional constant shift.
- `ts_skewness(x, d)`: Return skewness of x for the past d days
- `ts_std_dev(x, d)`: Calculates the standard deviation of a data series x over the past d days, measuring how much the values deviate from their mean during that period.
- `ts_step(1)`: Returns a counter of days, incrementing by one each day.
- `ts_sum(x, d)`: Sum values of x for the past d days.
- `ts_target_tvr_decay(x, lambda_min=0, lambda_max=1, target_tvr=0.1)`: Tune "ts_decay" to have a turnover equal to a certain target, with optimization weight range between lambda_min, lambda_max
- `ts_zscore(x, d)`: Calculates the Z-score of a time series, showing how far today's value is from the recent average, measured in standard deviations. Useful for standardizing and comparing values over time.

### Transformational

- `bucket(rank(x), range=“0, 1, 0.1”, skipBoth=False, NaNGroup=False)
or
bucket(rank(x), buckets = “2,5,6,7,10”, skipBoth=False, NaNGroup=False)`: The bucket operator creates custom groups by dividing data into buckets (ranges) based on ranked values of any data field. These buckets can then be used with group operators like group_neutralize, group_rank, group_zscore etc.
- `trade_when(x, y, z)`: The trade_when operator changes Alpha values only when a specific condition is met, keeps previous values otherwise, and can close positions by assigning NaN under an exit condition. It is useful for reducing turnover and controlling when trades are executed.

### Vector

- `vec_avg(x)`: Calculates the mean (average) of all elements in a vector field for each instrument and date, converting vector data to a single matrix value.
- `vec_count(x)`: Number of elements in vector field x
- `vec_max(x)`: Maximum value form vector field x
- `vec_min(x)`: Minimum value form vector field x
- `vec_range(x)`: Difference between maximum and minimum element in vector field x
- `vec_stddev(x)`: Standard Deviation of vector field x
- `vec_sum(x)`: Calculates the sum of all values in a vector field.

## Recommended GPT Retrieval Contract

1. Lock the simulation settings first and reject fields outside the locked scope.
2. Select one or two datasets or a narrow category; do not search the full registry in the prompt.
3. Retrieve candidate fields with field_id, description, type, coverage, and dataset provenance.
4. Select only operators valid for the expression language and compatible with the selected field types.
5. Generate factor expressions, then run syntax / operator-count / setting validation before any backtest.
