'''
This file will be some strats I want to test for fun
'''
import numpy as np
import data
import gbm
import matplotlib.pyplot as plt

'''
Alternating IVV and QQQ day by day
'''
def daily_half_strat(n_paths=20):
    years = 30
    steps = years * 252
    ivv_shares = np.zeros(n_paths) #arrays for how many ivv and qqq shares in each run
    qqq_shares = np.zeros(n_paths)
    portfolio_value_over_time = np.zeros((steps, n_paths)) # tracks portfoilio value per day of each run so it can be plotted

    px, log_rets, mu, sigma, cov = data.get_gbm_calibration()
    S0 = px.iloc[-1].values
    paths = gbm.simulate_gbm_paths(S0, mu, cov, years, 252, n_paths)

    for i in range(7560):
        prices_i = paths[i] # all the prices of all the paths on that one given day

        if (i % 2 == 0):
            ivv_shares += (prices_i[0])/100 # buy $100 of IVV for each path

        else:
            qqq_shares += (prices_i[1])/100
        
        # portfolio value at time i
        portfolio_value_over_time[i] = (ivv_shares * prices_i[0] + qqq_shares * prices_i[1]) 


    plt.plot(portfolio_value_over_time[:,:], alpha=0.15)
    plt.show()
    return

daily_half_strat()
    
    