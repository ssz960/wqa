# Getting started with Insiders Datasets


Source: https://support.worldquantbrain.com/hc/en-us/community/posts/27493900685335-Getting-started-with-Insiders-Datasets


Tips for getting started with [Insiders](https://platform.worldquantbrain.com/data/data-sets?category=insiders) Datasets:

- This data category provides information on companies' insider trading activities. Although insider trading is strictly regulated in most markets, resulting in lower data coverage, it can still offer valuable insights.

This data category provides information on companies' insider trading activities. Although insider trading is strictly regulated in most markets, resulting in lower data coverage, it can still offer valuable insights.

- Corporate insiders usually have an information advantage over the general public. Therefore, when insiders increase their holdings in their own companies, it can be a positive signal, and vice versa.

Corporate insiders usually have an information advantage over the general public. Therefore, when insiders increase their holdings in their own companies, it can be a positive signal, and vice versa.

- Don't be overly concerned about low data coverage. Since insiders are required to disclose trades related to company stocks, there typically aren't many activities. However, when there is activity, it can offer high-quality information. Some backfilling techniques like ts_backfill() can be helpful, but avoid setting the backfill period too long.

Don't be overly concerned about low data coverage. Since insiders are required to disclose trades related to company stocks, there typically aren't many activities. However, when there is activity, it can offer high-quality information. Some backfilling techniques like ts_backfill() can be helpful, but avoid setting the backfill period too long.

- Most of the data fields are vector-type and need preprocessing before simulation. Instead of just using vec_avg(), consider using operators like vec_stddev() or vec_skewness(). These may be advantageous in extracting signals from the distribution/skewness within a day, especially for transaction and filing information.

Most of the data fields are vector-type and need preprocessing before simulation. Instead of just using vec_avg(), consider using operators like vec_stddev() or vec_skewness(). These may be advantageous in extracting signals from the distribution/skewness within a day, especially for transaction and filing information.

Example Alpha ideas:

- Insiders buying shares in their own company often indicates confidence in the company's future performance. Consider going long on stocks where insiders have recently made significant purchases, and short-selling stocks where insiders have recently sold a large number of shares.

Insiders buying shares in their own company often indicates confidence in the company's future performance. Consider going long on stocks where insiders have recently made significant purchases, and short-selling stocks where insiders have recently sold a large number of shares.

- Insider activity in medium to small-cap stocks can have a more pronounced impact on the stock price due to lower liquidity and market attention. Consider working on larger/less liquid universes like USA_TOP3000, ILLIQUID_MINVOL1M, or GLB_MINVOL1M.

Insider activity in medium to small-cap stocks can have a more pronounced impact on the stock price due to lower liquidity and market attention. Consider working on larger/less liquid universes like USA_TOP3000, ILLIQUID_MINVOL1M, or GLB_MINVOL1M.

Recommended Datasets:

- [Global Insider Trading Data](https://platform.worldquantbrain.com/data/data-sets/insiders1)

- [Edgar forms data](https://platform.worldquantbrain.com/data/data-sets/insiders4)
