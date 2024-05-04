if __name__ == "__main__":
    from utilities import *

    # df0 = ugr_load_data("june", 1)
    df1 = ugr_load_data("june", 2)
    # df2 = ugr_load_data("june", 3)
    df = ugr_concat_data_list([df1])
    # df = ugr_crop_few_minutes(df, 10, 10)
    df = ugr_get_first_n_days(df, 1)
    
    dff = ugr_get_few_minutes(df, 10*60-1-9/60, 15)
    
    print(dff)

    from matplotlib import pyplot as plt
    import numpy as np
    import pandas as pd
    from diff_utils import *
    plt.rcParams['axes.grid'] = True
    plt.figure(figsize=(12, 5))

    dff1 = dff.copy()
    dff2 = dff.copy()

    bitrate = smooth(dff["Bitrate"], 10)
    bitrate_attack_spike = smooth(apply_attack(dff1, 2, 0)["Bitrate"], 10)
    bitrate_attack_gradual = smooth(apply_attack(dff2, 2, 1)["Bitrate"], 10)

    ossef = 0

    # Plot all three series in the same plot with different colors and legends
    plt.plot(dff["Date"][ossef:], bitrate_attack_spike[ossef:], color="red")
    plt.plot(dff["Date"][ossef:], bitrate_attack_gradual[ossef:], color="orange")
    plt.plot(dff["Date"], bitrate, color="black")
    plt.vlines(dff["Date"][720], 0, 4*10**8, color="red", linestyle="--")

    plt.legend(["Bitrate spike attack", "Bitrate gradual attack", "Bitrate original", "Window separator"])
    plt.xlabel("Time")
    plt.ylabel("Bitrate")
    plt.savefig("plot_attack.svg")
