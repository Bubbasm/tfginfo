def ugr_load_data(month: str, weekNum: int):
    import pandas as pd

    if month not in ["march", "april", "may", "june", "july", "august"]:
        print("Invalid month")
        return

    columns = ["Date", "Bitrate", "Packet rate"]
    try:
        df = pd.read_csv('../../datasets/ugr16/'+month+'_week'+str(weekNum)+'_csv/BPSyPPS.txt', sep=',', names=columns)
    except FileNotFoundError:
        print("File not found")
        return
    df["Date"] = pd.to_datetime(df["Date"], unit='s')
    

    return df

def ugr_concat_data(data1, data2):
    import pandas as pd
    data1Idx = len(data1)-1
    data2Idx = 0

    if data1["Date"][data1Idx] >= data2["Date"][data2Idx]:
        data1 = data1.copy()

    while data1["Date"][data1Idx] >= data2["Date"][data2Idx]:
        data2Idx += 1

    while data2Idx >= 0:
        if data1["Date"][data1Idx] == data2["Date"][data2Idx]:
            data1.loc[data1Idx, "Bitrate"] += data2.loc[data2Idx, "Bitrate"]
            data1.loc[data1Idx, "Packet rate"] += data2.loc[data2Idx, "Packet rate"]
            data1Idx -= 1
            data2Idx -= 1
        elif data1["Date"][data1Idx] > data2["Date"][data2Idx]:
            data1Idx -= 1
        else:
            data2Idx -= 1

    data2 = data2[data2["Date"] > data1["Date"].iloc[-1]]

    df = pd.concat([data1, data2], ignore_index=True)

    return df

def ugr_concat_data_list(dataList):
    if len(dataList) == 0:
        return
    import pandas as pd
    df = dataList[0]
    for i in range(1, len(dataList)):
        df = ugr_concat_data(df, dataList[i])
    return df

def smooth(a,WSZ):
    if WSZ == 1:
        return a
    import numpy as np
    out0 = np.convolve(a,np.ones(WSZ,dtype=int),'valid')/WSZ    
    r = np.arange(1,WSZ-1,2)
    start = np.cumsum(a[:WSZ-1])[::2]/r
    stop = (np.cumsum(a[:-WSZ:-1])[::2]/r)[::-1]
    return np.concatenate((  start , out0, stop  ))

def crop_few_minutes(df, minutesLeft, minutesRight=None):
    import pandas as pd
    if minutesRight == None:
        minutesRight = minutesLeft
    df = df[df["Date"] > df["Date"][0] + pd.Timedelta(minutes=minutesLeft)]
    df.reset_index(drop=True, inplace=True)
    df = df[df["Date"] < df["Date"][len(df)-1] - pd.Timedelta(minutes=minutesRight)]
    df.reset_index(drop=True, inplace=True)
    return df

def ugr_simple_plot(df, smoothingWindow=60*10+1, plotColumns=["Bitrate", "Packet rate"], separateWeeks=True):
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    import pandas as pd
    import numpy as np
    from datetime import datetime

    colorPalette = ["#165091", "#E16E0D", "#26890C", "#1368CE", "#D62728", "#8C564B", "#E377C2", "#7F7F7F", "#BCBD22", "#17BECF"]

    if smoothingWindow % 2 == 0:
        smoothingWindow += 1

    plt.rcParams['axes.grid'] = True

    if separateWeeks:
        weeks = [g for n, g in df.groupby(pd.Grouper(key='Date',freq='W')) if len(g) > 0]
        [week.reset_index(drop=True, inplace=True) for week in weeks]
    else:
        weeks = [df]

    axCount = len(plotColumns)*len(weeks)
    
    fig, axs = plt.subplots(axCount, 1, figsize=(16, 9))
    if axCount == 1:
        axs = [axs]
    plt.subplots_adjust(left=0.1, bottom=0.25)

    for weekIdx in range(len(weeks)):
        week = weeks[weekIdx]
        for plotColIdx in range(len(plotColumns)):
            plotCol = plotColumns[plotColIdx]
            for ax in axs[plotColIdx*len(weeks)+weekIdx::axCount]:
                color = colorPalette.pop(0)
                colorPalette.append(color)
                ax.plot(week["Date"], smooth(week[plotCol], smoothingWindow), label=plotCol, color=color)
                ax.set_ylabel(plotCol)
                ax.set_xlabel("Date" + " (week "+str(week["Date"][0].week)+")")
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m/%d %A'))
                ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
                startWeek = datetime.strptime(str(week["Date"][0].year) + " " + str(week["Date"][0].week-1) + ' 0', "%Y %W %w")
                endWeek = datetime.strptime(str(week["Date"][0].year) + " " + str(week["Date"][0].week) + ' 0', "%Y %W %w")
                ax.set_xbound(pd.to_datetime(startWeek)+pd.Timedelta(days=1), pd.to_datetime(endWeek)+pd.Timedelta(days=1))
                ax.legend()
                ax.ticklabel_format(axis='y', style='sci', scilimits=(8,4))

    fig.tight_layout()
    plt.show()