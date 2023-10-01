from holt_winters import *
import numpy as np

def smooth(a,WSZ):
    # a: NumPy 1-D array containing the data to be smoothed
    # WSZ: smoothing window size needs, which must be odd number,
    # as in the original MATLAB implementation
    out0 = np.convolve(a,np.ones(WSZ,dtype=int),'valid')/WSZ    
    r = np.arange(1,WSZ-1,2)
    start = np.cumsum(a[:WSZ-1])[::2]/r
    stop = (np.cumsum(a[:-WSZ:-1])[::2]/r)[::-1]
    return np.concatenate((  start , out0, stop  ))

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from datetime import datetime
    import matplotlib.dates as mdates
    import pandas as pd

    segsInDay = 86400
    movingAvgWindow = 60*10*1 + 1

    df = pd.read_csv(r'../../datasets/ugr16/june_week2_csv/BPSyPPS.txt', sep=',', names=["Date", "Bitrate", "Packet rate"])
    df["Date"] = pd.to_datetime(df["Date"], unit='s')

    twodays = df[df["Date"] < df["Date"][0] + pd.Timedelta(days=2)]
    threedays = df[df["Date"] < df["Date"][0] + pd.Timedelta(days=3)]
    print(threedays)
    param="Bitrate"

    alpha, beta, gamma = 0.44425, 0.00015,0.10659
    alpha, beta, gamma= 0.01158, 0.00137, 0.92863
    alpha, beta, gamma= 0.64087, 0.00065, 0.20647
    alpha, beta, gamma= 0.47113, 0.00058, 0.09931
    alpha, beta, gamma= 0.55569, 0.01525, 0.86588
    alpha, beta, gamma= 0.19307, 0.02003, 0.71383
    alpha, beta, gamma= 0.13761, 0.27705, 0.33215
    alpha, beta, gamma= 0.4481, 0.0, 0.74945
    alpha, beta, gamma= 0.72149, 0.00004, 0.17637
    rate = triple_exponential_smoothing(twodays[param], segsInDay, alpha, beta, gamma, segsInDay)

    plt.figure(figsize=(16,9))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y %H:%M:%S'))
    plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
    
    plt.plot(threedays["Date"], smooth(rate, movingAvgWindow), color="#1368CE", label="Holt-Winters")
    plt.plot(threedays["Date"], smooth(threedays[param], movingAvgWindow), color="#26890C", label="Real")
    plt.plot(threedays["Date"], smooth(rate-threedays[param], movingAvgWindow), color="#E21B3C", label="Error")
    print("%.3E"%(np.sqrt(sum((threedays[param]-rate)**2))))
    plt.gcf().autofmt_xdate()

    plt.title("Triple Exponential Smoothing")
    plt.legend(loc="lower right")
    plt.xlabel("Time")
    plt.ylabel("Value")

    plt.show()