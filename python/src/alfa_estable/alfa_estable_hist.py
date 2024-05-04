if __name__ == "__main__":
    import numpy as np
    import pandas as pd
    from scipy.stats import levy_stable
    from utilities import *
    from diff_utils import *
    from matplotlib import pyplot as plt
    plt.rcParams['axes.grid'] = True

    # df1 = ugr_load_data("june", 2)
    # df2 = ugr_load_data("june", 3)

    # df = ugr_concat_data_list([df1, df2])
    # # df = ugr_crop_few_minutes(df, 10)

    # dff = ugr_get_few_minutes(df, 60-1-9/60, 15)

    # dff1 = apply_attack(dff.copy(), 2, 0)
    # dff2 = apply_attack(dff.copy(), 2, 1)

    # x0_t = dff["Bitrate"].values
    # x0_t0 = diff_series(dff, method=0)
    # x0_t1 = diff_series(dff, method=1)
    # x1_t = dff1["Bitrate"].values
    # x1_t0 = diff_series(dff1, method=0)
    # x1_t1 = diff_series(dff1, method=1)
    # x2_t = dff2["Bitrate"].values
    # x2_t0 = diff_series(dff2, method=0)
    # x2_t1 = diff_series(dff2, method=1)

    readtabl = pd.read_csv("../matlab/ventana_test_norm.csv")
    x0_t0 = readtabl["x0_t0_norm"].values
    x0_t0 = x0_t0[~np.isnan(x0_t0)]
    x0_t1 = readtabl["x0_t1_norm"].values
    x0_t1 = x0_t1[~np.isnan(x0_t1)]
    x1_t0 = readtabl["x1_t0_norm"].values
    x1_t0 = x1_t0[~np.isnan(x1_t0)]
    x1_t1 = readtabl["x1_t1_norm"].values
    x1_t1 = x1_t1[~np.isnan(x1_t1)]
    x2_t0 = readtabl["x2_t0_norm"].values
    x2_t0 = x2_t0[~np.isnan(x2_t0)]
    x2_t1 = readtabl["x2_t1_norm"].values
    x2_t1 = x2_t1[~np.isnan(x2_t1)]

    fig, axs = plt.subplots(2, 3, figsize=(16, 10))

    bincount = 100

    def levy_stable_samples(alpha, beta, gamma, delta, size):
        return levy_stable.rvs(alpha=alpha, beta=beta, loc=0, scale=1, size=size)

    x0_t0_alpha, x0_t0_beta, x0_t0_gamma, x0_t0_delta = 1.226665042416467, -0.021354736859829, 1, 0 # 1.085944934107338e+07, 1.172261273861246e+05
    x0_t1_alpha, x0_t1_beta, x0_t1_gamma, x0_t1_delta = 1.379591777387362, 0.030561574307348, 1, 0 # 7.912299067972941e+06, -7.278791546942558e+05
    x1_t0_alpha, x1_t0_beta, x1_t0_gamma, x1_t0_delta = 1.221843045619104, -0.030485847885997, 1, 0 # 1.084931651682431e+07, 4.278545578874534e+05
    x1_t1_alpha, x1_t1_beta, x1_t1_gamma, x1_t1_delta = 1.373241366034431, 0.028688913638621, 1, 0 # 7.914434533144827e+06, -5.258290108851925e+05
    x2_t0_alpha, x2_t0_beta, x2_t0_gamma, x2_t0_delta = 1.226905331230766, -0.020004304960309, 1, 0 # 1.087044237847402e+07, 1.160054197892209e+05
    x2_t1_alpha, x2_t1_beta, x2_t1_gamma, x2_t1_delta = 1.379591818619633, 0.033013729419128, 1, 0 # 7.921881222260477e+06, -7.210704465727936e+05

    x0_t0_levy = levy_stable_samples(x0_t0_alpha, x0_t0_beta, x0_t0_gamma, x0_t0_delta, len(x0_t0))
    x0_t0_levy = x0_t0_levy[abs(x0_t0_levy-x0_t0_delta) < np.percentile(x0_t0_levy-x0_t0_delta, 99)]
    x0_t1_levy = levy_stable_samples(x0_t1_alpha, x0_t1_beta, x0_t1_gamma, x0_t1_delta, len(x0_t1))
    x0_t1_levy = x0_t1_levy[abs(x0_t1_levy-x0_t1_delta) < np.percentile(x0_t1_levy-x0_t1_delta, 99)]
    x1_t0_levy = levy_stable_samples(x1_t0_alpha, x1_t0_beta, x1_t0_gamma, x1_t0_delta, len(x1_t0))
    x1_t0_levy = x1_t0_levy[abs(x1_t0_levy-x1_t0_delta) < np.percentile(x1_t0_levy-x1_t0_delta, 99)]
    x1_t1_levy = levy_stable_samples(x1_t1_alpha, x1_t1_beta, x1_t1_gamma, x1_t1_delta, len(x1_t1))
    x1_t1_levy = x1_t1_levy[abs(x1_t1_levy-x1_t1_delta) < np.percentile(x1_t1_levy-x1_t1_delta, 99)]
    x2_t0_levy = levy_stable_samples(x2_t0_alpha, x2_t0_beta, x2_t0_gamma, x2_t0_delta, len(x2_t0))
    x2_t0_levy = x2_t0_levy[abs(x2_t0_levy-x2_t0_delta) < np.percentile(x2_t0_levy-x2_t0_delta, 99)]
    x2_t1_levy = levy_stable_samples(x2_t1_alpha, x2_t1_beta, x2_t1_gamma, x2_t1_delta, len(x2_t1))
    x2_t1_levy = x2_t1_levy[abs(x2_t1_levy-x2_t1_delta) < np.percentile(x2_t1_levy-x2_t1_delta, 99)]

    x0_t0 = x0_t0[abs(x0_t0-x0_t0.mean()) < np.percentile(x0_t0-x0_t0.mean(), 99)]
    x0_t1 = x0_t1[abs(x0_t1-x0_t1.mean()) < np.percentile(x0_t1-x0_t1.mean(), 99)]
    x1_t0 = x1_t0[abs(x1_t0-x1_t0.mean()) < np.percentile(x1_t0-x1_t0.mean(), 99)]
    x1_t1 = x1_t1[abs(x1_t1-x1_t1.mean()) < np.percentile(x1_t1-x1_t1.mean(), 99)]
    x2_t0 = x2_t0[abs(x2_t0-x2_t0.mean()) < np.percentile(x2_t0-x2_t0.mean(), 99)]
    x2_t1 = x2_t1[abs(x2_t1-x2_t1.mean()) < np.percentile(x2_t1-x2_t1.mean(), 99)]

    # plot 6 histograms
    axs[0, 0].set_title("No Attack")
    axs[0, 0].hist(x0_t0, bins=bincount, density=True, alpha=0.5, label='Discrete difference')
    axs[0, 0].hist(x0_t0_levy, bins=bincount, density=True, alpha=0.5, label='Alpha-Stable fit')
    axs[0, 0].legend()
    axs[1, 0].set_title("No Attack")
    axs[1, 0].hist(x0_t1, bins=bincount, density=True, alpha=0.5, label='Convolution')
    axs[1, 0].hist(x0_t1_levy, bins=bincount, density=True, alpha=0.5, label='Alpha-Stable fit')
    axs[1, 0].legend()

    axs[0, 1].set_title("Spike Attack")
    axs[0, 1].hist(x1_t0, bins=bincount, density=True, alpha=0.5, label='Discrete difference')
    axs[0, 1].hist(x1_t0_levy, bins=bincount, density=True, alpha=0.5, label='Alpha-Stable fit')
    axs[0, 1].legend()
    axs[1, 1].set_title("Spike Attack")
    axs[1, 1].hist(x1_t1, bins=bincount, density=True, alpha=0.5, label='Convolution')
    axs[1, 1].hist(x1_t1_levy, bins=bincount, density=True, alpha=0.5, label='Alpha-Stable fit')
    axs[1, 1].legend()

    axs[0, 2].set_title("Incremental Attack")
    axs[0, 2].hist(x2_t0, bins=bincount, density=True, alpha=0.5, label='Discrete difference')
    axs[0, 2].hist(x2_t0_levy, bins=bincount, density=True, alpha=0.5, label='Alpha-Stable fit')
    axs[0, 2].legend()
    axs[1, 2].set_title("Incremental Attack")
    axs[1, 2].hist(x2_t1, bins=bincount, density=True, alpha=0.5, label='Convolution')
    axs[1, 2].hist(x2_t1_levy, bins=bincount, density=True, alpha=0.5, label='Alpha-Stable fit')
    axs[1, 2].legend()

    fig.supylabel("Density")
    fig.supxlabel("Bitrate increment")

    # save all x0_t0, ... series to ventana_test.csv
    # pd.DataFrame({
    #     "x0_t0": x0_t0,
    #     "x0_t1": x0_t1,
    #     "x1_t0": x1_t0,
    #     "x1_t1": x1_t1,
    #     "x2_t0": x2_t0,
    #     "x2_t1": x2_t1,
    # }).to_csv("ventana_test.csv", index=False)

    


    plt.tight_layout()
    plt.savefig("alfa_estable_norm_hist.svg")
    # plt.show()