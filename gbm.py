'''
This file will simulate future prices using geometric brownian motion based on
the parameters we get from data.py. We will do this through the gbm formula
'''

import numpy as np

'''
The data we get from data.py is annual and since we are simulating daily change 
we need to convert it
'''
def convert_annual_to_daily(mu_annual, cov_annual, steps_per_year=252):
    dt = 1 / steps_per_year # we need dt to scale everything, it's just the change in time per step
    mu = mu_annual * dt
    cov = cov_annual * dt # we will use this to make the stochastic shock
    return mu, cov, dt


def simulate_gbm_paths(S0, mu_annual, cov_annual, years=30, steps_per_year=252, n_paths=5000):
    mu, cov, dt = convert_annual_to_daily(mu_annual, cov_annual, steps_per_year)
    n_steps = years * steps_per_year
    n_assets = len(S0)

    paths = np.zeros((n_steps + 1, n_assets, n_paths)) # this makes a 3 dimensional array because we put in one argument which is the shape
    paths[0] = S0[:, None] # making all the first time steps have the initial price


    # using cholesky decomposition for correlated gbm shocks
    # cholesky only works if |p| < 1 which basically will work for everything
    L = np.linalg.cholesky(cov)
    drift = mu - (np.diag(cov)/2) # drift term in the exponential in the formula

    for t in range(1, n_steps + 1):
        