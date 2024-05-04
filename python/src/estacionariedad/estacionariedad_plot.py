if __name__ == "__main__":
    from utilities import *
    from diff_utils import *
    from matplotlib import pyplot as plt
    plt.rcParams['axes.grid'] = True

    df1 = ugr_load_data("june", 2)
    df2 = ugr_load_data("june", 3)

    df = ugr_concat_data_list([df1, df2])
    # df = ugr_crop_few_minutes(df, 10)


    dff = ugr_get_few_minutes(df, 10*60-1-9/60, 15)

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

    fig, axs = plt.subplots(3, 1, figsize=(16, 10))

    smoothness = 1
    
    axs[0].plot(dff1["Date"][-130:], x1_t[-130:], label="Bitrate spike attack", color="red")
    axs[0].plot(dff2["Date"][-130:], x2_t[-130:], label="Bitrate incremental attack", color="orange")
    axs[0].plot(dff["Date"][-130:], x0_t[-130:], label="Bitrate", color="black")
    axs[0].set_title("Original")
    axs[0].legend()
    axs[1].plot(dff1["Date"][:-1][-130:], x1_t0[-130:], label="Bitrate spike attack", color="red")
    axs[1].plot(dff2["Date"][:-1][-130:], x2_t0[-130:], label="Bitrate incremental attack", color="orange")
    axs[1].plot(dff["Date"][:-1][-130:], x0_t0[-130:], label="Bitrate", color="black")
    axs[1].set_title("First order differenciation")
    axs[1].legend()
    axs[2].plot(dff1["Date"][1:-1][-130:], x1_t1[-130:], label="Bitrate spike attack", color="red")
    axs[2].plot(dff2["Date"][1:-1][-130:], x2_t1[-130:], label="Bitrate incremental attack", color="orange")
    axs[2].plot(dff["Date"][1:-1][-130:], x0_t1[-130:], label="Bitrate", color="black")
    axs[2].set_title("Convolution differenciation")
    axs[2].legend()

    print(x0_t.mean(), x0_t.std())

    x0_0 = (((x0_t0[720:] - x0_t0[:720].mean()) / x0_t0[:720].std()).mean())
    x0_1 = (((x0_t1[720:] - x0_t1[:720].mean()) / x0_t1[:720].std()).mean())
    x1_0 = (((x1_t0[720:] - x1_t0[:720].mean()) / x1_t0[:720].std()).mean())
    x1_1 = (((x1_t1[720:] - x1_t1[:720].mean()) / x1_t1[:720].std()).mean())
    x2_0 = (((x2_t0[720:] - x2_t0[:720].mean()) / x2_t0[:720].std()).mean())
    x2_1 = (((x2_t1[720:] - x2_t1[:720].mean()) / x2_t1[:720].std()).mean())

    print(x0_0, x0_1)
    print(x1_0, x1_1)
    print(x2_0, x2_1)

    plt.xlabel("Time")
    plt.tight_layout()
    # plt.savefig("estacionariedad_plot_attack.svg")
    plt.show()