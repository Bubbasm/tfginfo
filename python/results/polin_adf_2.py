if __name__ == "__main__":
    from utilities import *
    import numpy as np
    from statsmodels.tsa.stattools import adfuller, kpss
    import warnings
    from statsmodels.tools.sm_exceptions import InterpolationWarning
    warnings.simplefilter('ignore', InterpolationWarning)
    import matplotlib.pyplot as plt
    from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

    df1 = ugr_load_data("june", 2)
    df2 = ugr_load_data("june", 3)
    df = ugr_concat_data_list([df1, df2])
    df = ugr_crop_few_minutes(df, 10, 10)

    
    # compactSize = 1
    winlen = 60*10 # minutes

    dff = ugr_get_few_minutes(df, 10, winlen)
    # dff = ugr_group_n_points(dff, compactSize)

    y_t = dff["Bitrate"]
    x_t = dff["Bitrate"].diff().dropna().reset_index(drop=True, inplace=False)
    x_adf = adfuller(x_t)
    print(x_adf)
    x_kpss = kpss(x_t)
    print(x_kpss)
    fig, axs = plt.subplots(nrows=1, ncols=1, figsize=(10, 4), sharex=True)
    # plot_acf(y_t, ax=axs, alpha=0.05)
    # axs.set_title('Autocorrelación serie original')
    # plot_acf(x_t, ax=axs, lags=60, alpha=0.05)
    # axs.set_title('Autocorrelación serie diferenciada (order=1)')

    # plt.tight_layout()
    # plt.show()

    # y_adf = adfuller(y_t, maxlag=86400/compactSize)
    # print(y_adf)
    # y_kpss = kpss(y_t)
    # print(y_kpss)
    # if y_adf[1] < 0.05 and y_kpss[1] > 0.05:
    #     print("Stationary")
    #     exit

    # x_adf = adfuller(x_t)
    # print(x_adf)
    # x_kpss = kpss(x_t)
    # print(x_kpss)
    # if x_adf[1] > 0.05 or x_kpss[1] < 0.05:
    #     print("Not stationary with diff")




# Con 2 dias:
# adf: (-8.730849047560607, 3.194768552584953e-14, 77, 172722, {'1%': -3.4303878608236804, '5%': -2.8615567339685435, '10%': -2.5667789068923654}, 6277239.3522311)
# kpss: (5.12373933198176, 0.01, 235, {'10%': 0.347, '5%': 0.463, '2.5%': 0.574, '1%': 0.739})
# adf pasa, pero kpss no pasa --> hay tendencia y no es estacionaria

# Con 6 dias:
# adf: (-14.467536590883565, 6.6884584713109e-27, 100, 518299, {'1%': -3.430362616911063, '5%': -2.8615455765266176, '10%': -2.5667729681813385}, 18787305.87878092)
# kpss: (18.461350394314678, 0.01, 401, {'10%': 0.347, '5%': 0.463, '2.5%': 0.574, '1%': 0.739})
# igual
# Pero si hacemos diferenciacion de orden 1:
# (-94.44953421190141, 0.0, 99, 518299, {'1%': -2.5657443137397484, '5%': -1.9410005182462098, '10%': -1.6168194875645838}, 18787459.97587136)
# (0.004602580315173691, 0.1, 1793, {'10%': 0.347, '5%': 0.463, '2.5%': 0.574, '1%': 0.739})
# adf pasa y kpss tambien pasa --> estacionaria

# Con 6 dias, pero cambiando la unidad de tiempo de 1 segundo a 2 minutos forzando maxlag a 1 dia:
# adf: (1.323844608497929, 0.996739162805519, 720, 3599, {'1%': -3.4321682745778963, '5%': -2.86234341192807, '10%': -2.56719766893431}, 4.442707865815035)
# kpss: (1.1052512853176921, 0.01, 39, {'10%': 0.347, '5%': 0.463, '2.5%': 0.574, '1%': 0.739})
# diferenciando:
# adf: (-15.45344039509425, 3.541595377470256e-27, 30, 4288, {'1%': -2.566261605841623, '5%': -1.941062822539652, '10%': -1.6167582069845259}, 196899.69071856354)
# kpss: (0.01766206577989663, 0.1, 79, {'10%': 0.347, '5%': 0.463, '2.5%': 0.574, '1%': 0.739})
