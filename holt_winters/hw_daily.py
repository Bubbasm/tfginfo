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
    from datetime import datetime
    from matplotlib.widgets import Slider
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    import pandas as pd
    import numpy as np
    import time


    segsInDay = 86400
    movingAvgWindow = 60*10 + 1

    df0 = pd.read_csv(r'../../datasets/ugr16/june_week2_csv/BPSyPPS.txt', sep=',', names=["Date", "Bitrate", "Packet rate"])
    # df1 = pd.read_csv(r'../../datasets/ugr16/june_week2_csv/BPSyPPS.txt', sep=',', names=["Date", "Bitrate", "Packet rate"])
    # Add "Bitrate" and "Packet rate" in df0 for values of df1 that match on "Date"
    # df1 = df1[df1["Date"] > df0["Date"][len(df0)-1]]
    df = pd.concat([df0], ignore_index=True)
    df["Date"] = pd.to_datetime(df["Date"], unit='s')

    dfNew = df
    # dfNew = df[df["Date"][0] + pd.Timedelta(days=0.1) < df["Date"]]
    # dfNew.reset_index(drop=True, inplace=True)
    twodays = dfNew[dfNew["Date"] < dfNew["Date"][0] + pd.Timedelta(days=2)]
    threedays = dfNew[dfNew["Date"] < dfNew["Date"][0] + pd.Timedelta(days=3)]
    param="Packet rate"


    alpha, beta, gamma= 0.39081, 0.0, 0.42234
    alpha, beta, gamma= 0.2940, 0.092, 0.422
    alpha, beta, gamma= 0.39081, 0.0, 0.42234
    rate = triple_exponential_smoothing(twodays[param], segsInDay, alpha, beta, gamma, segsInDay)

    fig, ax = plt.subplots(figsize=(16,9))
    plt.subplots_adjust(left=0.1, bottom=0.25)
    
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y %H:%M:%S'))
    plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
    
    plt.title("Triple Exponential Smoothing")
    plt.legend(["This is my legend"], fontsize="x-large")
    plt.xlabel("Time")
    plt.ylabel("Value")


    line1, = plt.plot(threedays["Date"], smooth(rate, movingAvgWindow), color="#1368CE", label="Holt-Winters")
    line2, = plt.plot(threedays["Date"], smooth(threedays[param], movingAvgWindow), color="#26890C", label="Real")
    line3, = plt.plot(threedays["Date"], smooth(rate - threedays[param], movingAvgWindow), color="#E21B3C", label="Error")
    print("%.3E"%(np.sqrt(sum((threedays[param][-segsInDay:]-rate[-segsInDay:])**2))))
    # plt.gcf().autofmt_xdate()

    axcolor = 'lightgoldenrodyellow'
    axalpha = plt.axes([0.1, 0.1, 0.65, 0.03], facecolor=axcolor)
    axbeta = plt.axes([0.1, 0.05, 0.65, 0.03], facecolor=axcolor)
    axgamma = plt.axes([0.1, 0.00, 0.65, 0.03], facecolor=axcolor)

    s_alpha = Slider(axalpha, 'Alpha', 0.0, 1.0, valinit=alpha)
    s_beta = Slider(axbeta, 'Beta', 0.0, 1.0, valinit=beta)
    s_gamma = Slider(axgamma, 'Gamma', 0.0, 1.0, valinit=gamma)

    def update(val):
        alpha = s_alpha.val
        beta = s_beta.val
        gamma = s_gamma.val

        # Recalculate rate with updated alpha, beta, and gamma
        rate = triple_exponential_smoothing(twodays[param], segsInDay, alpha, beta, gamma, segsInDay)

        # Update plot data
        line1.set_ydata(smooth(rate, movingAvgWindow))
        line3.set_ydata(smooth(rate - threedays[param], movingAvgWindow))

        # Print the error
        print("%.3E" % (np.sqrt(sum((threedays[param] - rate) ** 2))))

        # Redraw the plot
        fig.canvas.draw_idle()
        plt.savefig("holt_winters"+str(int(time.time()))+".png")


    # Attach the update function to the sliders
    s_alpha.on_changed(update)
    s_beta.on_changed(update)
    s_gamma.on_changed(update)


    plt.savefig("holt_winters.png")
    plt.show()
