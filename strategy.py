'''
This file will be some strats I want to test for fun
'''
import numpy as np
import data
import gbm
import matplotlib.pyplot as plt


'''
helper method for computing risk metrics it will compute
the return volatility of the strategy and also the 
expected shortfall which will tell us how bad the average
crash is in the worst 5% of cases
'''
def compute_risk_metrics(portfolio_value_over_time, es_quantile=5):
    # this is essentially "shifting" the matrix and dividing each day by the previous day to get returns
    daily_returns = portfolio_value_over_time[1:] / portfolio_value_over_time[:-1] - 1
    volatility = np.std(daily_returns)

    return



'''
Alternating IVV and QQQ day by day
'''
def daily_half_strat(n_paths=1000):
    years = 30
    steps = years * 252
    ivv_shares = np.zeros(n_paths) #arrays for how many ivv and qqq shares in each run
    qqq_shares = np.zeros(n_paths)
    portfolio_value_over_time = np.zeros((steps, n_paths)) # tracks portfoilio value per day of each run so it can be plotted

    px, log_rets, mu, sigma, cov = data.get_gbm_calibration()
    S0 = px.iloc[-1].values
    paths = gbm.simulate_gbm_paths(S0, mu, cov, years, 252, n_paths)

    for i in range(steps):
        prices_i = paths[i] # all the prices of all the paths on that one given day

        if (i % 2 == 0):
            ivv_shares += (prices_i[0])/100 # buy $100 of IVV for each path

        else:
            qqq_shares += (prices_i[1])/100
        
        # portfolio value at time i
        portfolio_value_over_time[i] = (ivv_shares * prices_i[0] + qqq_shares * prices_i[1]) 


    #plt.plot(portfolio_value_over_time[:,:], alpha=0.15)
    #plt.show()
    median_path = np.median(portfolio_value_over_time, axis=1)

    return median_path

'''
buying only IVV
'''
def buyIVV(n_paths=1000):
    years = 30
    steps = years*252
    ivv_shares = np.zeros(n_paths)
    portfolio_value_over_time = np.zeros((steps, n_paths))

    px, log_rets, mu, sigma, cov = data.get_gbm_calibration()
    S0 = px.iloc[-1].values
    paths = gbm.simulate_gbm_paths(S0, mu, cov, years, 252, n_paths)

    for i in range(steps):
        prices_i = paths[i]
        ivv_shares += (prices_i[0])/100
        portfolio_value_over_time[i] = ivv_shares * prices_i[0]

    #plt.plot(portfolio_value_over_time[:,:], alpha=0.15)
    #plt.show()
    median_path = np.median(portfolio_value_over_time, axis=1)

    return median_path

'''
buy only qqq
'''
def buyQQQ(n_paths=1000):
    years = 30
    steps = years*252
    qqq_shares = np.zeros(n_paths)
    portfolio_value_over_time = np.zeros((steps, n_paths))

    px, log_rets, mu, sigma, cov = data.get_gbm_calibration()
    S0 = px.iloc[-1].values
    paths = gbm.simulate_gbm_paths(S0, mu, cov, years, 252, n_paths)

    for i in range(steps):
        prices_i = paths[i]
        qqq_shares += (prices_i[1])/100
        portfolio_value_over_time[i] = qqq_shares * prices_i[1]

    #plt.plot(portfolio_value_over_time[:,:], alpha=0.15)
    #plt.show()

    median_path = np.median(portfolio_value_over_time, axis=1)

    return median_path


'''
buying qqq only in bear markets
'''
def bear_buying(n_paths=1000):
    years = 30
    steps = years*252
    ivv_shares = np.zeros(n_paths)
    qqq_shares = np.zeros(n_paths)
    portfolio_value_over_time = np.zeros((steps, n_paths))
    px, log_rets, mu, sigma, cov = data.get_gbm_calibration()
    S0 = px.iloc[-1].values
    qqq_ath = np.full(n_paths, S0[1]) # initial all time high

    paths = gbm.simulate_gbm_paths(S0, mu, cov, years, 252, n_paths)

    for i in range(steps):
        price_ivv = paths[i, 0, :]
        price_qqq = paths[i, 1, :]

        qqq_ath = np.maximum(qqq_ath, price_qqq) # updates all time high for all paths
        buy_qqq_mask = price_qqq <= 0.85 * qqq_ath 
        buy_ivv_mask = ~buy_qqq_mask # inverse of qqq mask

        # buy qqq in the paths that fulfil the boolean condition in the mask
        qqq_shares[buy_qqq_mask] += 100/price_qqq[buy_qqq_mask]
        # buy ivv in all other paths
        ivv_shares[buy_ivv_mask] += 100/price_ivv[buy_ivv_mask]
        portfolio_value_over_time[i] = (ivv_shares * price_ivv + qqq_shares * price_qqq) 



    #plt.plot(portfolio_value_over_time[:,:], alpha=0.15)
    #plt.show()
    median_path = np.median(portfolio_value_over_time, axis=1)
    return median_path


    
