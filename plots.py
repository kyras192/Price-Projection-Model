'''
This file will be a visual representation of the monte carlo simulations
'''

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import data
import gbm

'''

px, log_rets, mu, sigma, cov = data.get_gbm_calibration()
S0 = px.iloc[-1].values
paths = gbm.simulate_gbm_paths(S0, mu, cov, 30, 252, 1000)

ivv = paths[:,0,:] # all ivv prices in all paths
qqq = paths[:,1,:] # all qqq prices in all paths

plt.plot(ivv, color="blue", alpha=0.03)
plt.show()

plt.plot(qqq, color="orange", alpha=0.1)
plt.show()

I did some testing for a while to see if the model produced expected outcomes
'''
