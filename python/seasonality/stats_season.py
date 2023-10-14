def smoothToSeries(a,WSZ):
    import pandas as pd
    # a: NumPy 1-D array containing the data to be smoothed
    # WSZ: smoothing window size needs, which must be odd number,
    # as in the original MATLAB implementation
    out0 = np.convolve(a,np.ones(WSZ,dtype=int),'valid')/WSZ    
    r = np.arange(1,WSZ-1,2)
    start = np.cumsum(a[:WSZ-1])[::2]/r
    stop = (np.cumsum(a[:-WSZ:-1])[::2]/r)[::-1]
    return pd.Series(np.concatenate((  start , out0, stop  )))

if __name__ == "__main__":
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    from statsmodels.tsa.seasonal import seasonal_decompose

    columns = ["Date", "Bitrate", "Packet rate"]
    paramMeasure="Bitrate"
    df = pd.read_csv(r'../../datasets/ugr16/june_week1_csv/BPSyPPS.txt', sep=',', names=columns)
    df["Date"] = pd.to_datetime(df["Date"], unit='s')

    df = df[df["Date"][0] + pd.Timedelta(days=1) < df["Date"]]
    df.sort_index(inplace=True)
    df.reset_index(drop=True, inplace=True)
    result = seasonal_decompose(x=df[paramMeasure], model='multiplicative', period=86400, extrapolate_trend='freq')
    fig, ax = plt.subplots(1, 1, sharex=True, figsize=(16,9))

    windowSize = 1

    smoothenObserv = smoothToSeries(result.observed.tolist(), windowSize)
    smoothenObserv.plot(ax=ax, legend=False, color='r')
    ax.set_ylabel('Observed')
    # smoothenTrend = smoothToSeries(result.trend.tolist(), windowSize)
    # smoothenTrend.plot(ax=axes[1], legend=False, color='g')
    # axes[1].set_ylabel('Trend')
    # smoothenSeason = smoothToSeries(result.seasonal.tolist(), windowSize)
    # smoothenSeason.plot(ax=axes[2], legend=False)
    # axes[2].set_ylabel('Seasonal')
    # smoothenResid = smoothToSeries(result.resid.tolist(), windowSize)
    # smoothenResid.plot(ax=axes[3], legend=False, color='k')
    # axes[3].set_ylabel('Residual')

    fig.show()
    fig.savefig('filename.eps', format='eps')

