import matplotlib.pyplot as plt
import strategy

qqq_returns, qqq_vol, qqq_es = strategy.buyQQQ()
ivv_returns, ivv_vol, ivv_es = strategy.buyIVV()
half_returns, half_vol, half_es = strategy.daily_half_strat()
bear_returns, bear_vol, bear_es = strategy.bear_buying()

def plot_strats():
    plt.plot(qqq_returns, color = "blue")
    plt.plot(ivv_returns, color = "orange")
    plt.plot(half_returns, color = "green")
    plt.plot(bear_returns, color = "red")
    plt.show()
    return 

def stats():
    print(f"qqq:\n{qqq_vol}\n{qqq_es}\n")
    print(f"ivv:\n{ivv_vol}\n{ivv_es}\n")
    print(f"half:\n{half_vol}\n{half_es}")
    print(f"bear:\n{bear_vol}\n{bear_es}")
    return


stats()