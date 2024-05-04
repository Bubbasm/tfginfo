if __name__ == "__main__":
    import numpy as np
    import pandas as pd
    from scipy.stats import levy_stable
    from utilities import *
    from diff_utils import *
    from matplotlib import pyplot as plt
    plt.rcParams['axes.grid'] = True

    df1 = ugr_load_data("june", 2)
    df2 = ugr_load_data("june", 3)

    df = ugr_concat_data_list([df1, df2])
    # df = ugr_crop_few_minutes(df, 10)

    dff = ugr_get_few_minutes(df, 60-1-9/60, 15)

    dff1 = apply_attack(dff.copy(), 2, 0)
    dff2 = apply_attack(dff.copy(), 2, 1)

    x0_t = dff["Bitrate"].values
    x0_t0 = diff_series(dff, method=0)
    x0_t1 = diff_series(dff, method=1)
    x1_t = dff1["Bitrate"].values
    x1_t0 = diff_series(dff1, method=0)
    x1_t1 = diff_series(dff1, method=1)
    x2_t = dff2["Bitrate"].values
    x2_t0 = diff_series(dff2, method=0)
    x2_t1 = diff_series(dff2, method=1)

    # normalize data
    x0_t0 = (x0_t0 - np.mean(x0_t0)) / np.std(x0_t0)
    x0_t1 = (x0_t1 - np.mean(x0_t1)) / np.std(x0_t1)
    x1_t0 = (x1_t0 - np.mean(x1_t0)) / np.std(x1_t0)
    x1_t1 = (x1_t1 - np.mean(x1_t1)) / np.std(x1_t1)
    x2_t0 = (x2_t0 - np.mean(x2_t0)) / np.std(x2_t0)
    x2_t1 = (x2_t1 - np.mean(x2_t1)) / np.std(x2_t1)

    fig, axs = plt.subplots(2, 3, figsize=(16, 10))

    bincount = 100

    # plot 6 histograms
    axs[0, 0].set_title("No Attack")
    axs[0, 0].hist(x0_t0, bins=bincount, density=True, alpha=0.5, label='Discrete difference')
    axs[0, 0].legend()
    axs[1, 0].set_title("No Attack")
    axs[1, 0].hist(x0_t1, bins=bincount, density=True, alpha=0.5, label='Convolution')
    axs[1, 0].legend()

    print(np.mean(x0_t0), np.std(x0_t0))
    print(np.mean(x0_t1), np.std(x0_t1))

    axs[0, 1].set_title("Spike Attack")
    axs[0, 1].hist(x1_t0, bins=bincount, density=True, alpha=0.5, label='Discrete difference')
    axs[0, 1].legend()
    axs[1, 1].set_title("Spike Attack")
    axs[1, 1].hist(x1_t1, bins=bincount, density=True, alpha=0.5, label='Convolution')
    axs[1, 1].legend()

    print(np.mean(x1_t0), np.std(x1_t0))
    print(np.mean(x1_t1), np.std(x1_t1))

    axs[0, 2].set_title("Incremental Attack")
    axs[0, 2].hist(x2_t0, bins=bincount, density=True, alpha=0.5, label='Discrete difference')
    axs[0, 2].legend()
    axs[1, 2].set_title("Incremental Attack")
    axs[1, 2].hist(x2_t1, bins=bincount, density=True, alpha=0.5, label='Convolution')
    axs[1, 2].legend()

    print(np.mean(x2_t0), np.std(x2_t0))
    print(np.mean(x2_t1), np.std(x2_t1))

    fig.supylabel("Density")
    fig.supxlabel("Bitrate increment")


    plt.tight_layout()
    plt.savefig("estandarizacion_hist.svg")
    # plt.show()