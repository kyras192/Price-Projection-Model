'''
This file is to basically calibrate the geometric brownian motion,
this will download the historical data for the S&P500 and the NASDAQ 100.
Hopefully we can use this data to get the parameters needed for the GBM which are
the average growth rate, volatility and correlation between the two assets.
We need correlation to make the simulations more realistic if we are testing
investment strategies because we don't want to run into scenarios where one is 
up 10% in a year and the other is down 30%.
'''

import numpy as np
import pandas as pd
import yfinance as yf


'''
Interesting thing I found while doing this: I was going to use indices for this but I noticed
there was a huge difference in the drift which seemed weird. However, if we account for the 
difference in dividends by using adjusted close (which only really affects etfs) we will get
a more accurate perception of the drift difference despite using less data
'''

# 2000 is the earliest start date that we can use if we want to overlap them with the same amount of data
def load_price_data(start = "2000-01-01", tickers = ["IVV", "QQQ"]):

    px = yf.download(tickers, start=start, auto_adjust=False)["Adj Close"].dropna()

    px.columns = ["S&P500", "NASDAQ100"]
    return px


# converts prices to log returns, the log of the %change in price, the formula is log(p_t/p_t-1)
# we want GBM so we will use log returns
# log returns make GBM more mathematically consistent and approximate normality better

def compute_log_returns(px):

    log_returns = np.log(px/px.shift(1))

    return log_returns.dropna()



'''calculates drift (mu), volatility vector (sigma) (we have a vector instead of a scalar because 
we have multiple assets and therefore a covariance matrix), covariance matrix 
'''
def calibrate_gbm_params(log_returns):

    mu_daily = log_returns.mean().values # average log return per day
    cov_daily = log_returns.cov().values # covariance matrix per day

    trading_days = 252
    mu_annual = mu_daily * trading_days # we are working with log returns so we multiply by trading days instead of using any exponents
    cov_annual = cov_daily * trading_days

    # the diagonal of the covariance matrix gives the variance so we just sqrt that for the volatility/sd
    sigma_annual = np.sqrt(np.diag(cov_annual))
    return mu_annual, sigma_annual, cov_annual



# this just does all the other functions at once 
def get_gbm_calibration(start = "2000-01-01"):

    px = load_price_data(start = start)
    log_returns = compute_log_returns(px)
    mu_annual, sigma_annual, cov_annual = calibrate_gbm_params(log_returns)
    return px, log_returns, mu_annual, sigma_annual, cov_annual




px, log_rets, mu, sigma, cov = get_gbm_calibration()

print("Historical Data")
print(px.tail())
print("\nAnnual Drift")
print(mu)
print("\nAnnual Volatility")
print(sigma)
print("\nAnnual Covariance Matrix")
print(cov)