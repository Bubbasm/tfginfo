if __name__ == "__main__":
    import pandas as pd
    from prophet import Prophet
    import matplotlib.pyplot as plt
    from utilities import *

    df = ugr_load_data("june", 2)
    # wavelets with prophet
    # param = "Bitrate"

    # (A1, D1) = pywt.dwt(df[param], "db1")
    # (A2, D2) = pywt.dwt(A1, "db1")
    
    # dfNew1 = pd.DataFrame(zip(df["Date"][::2], [a/1.5 for a in A1]), columns=["Date", param])
    # dfNew2 = pd.DataFrame(zip(df["Date"][::4], [a/2 for a in A2]), columns=["Date", param])

    # dfDiff = pd.DataFrame(zip(df["Date"][::4], [a/2 for a in D2]), columns=["Date", param])

    # df = dfNew2
    df.rename(columns={'Date': 'ds', 'Bitrate': 'y'}, inplace=True)

    model = Prophet()
    model.fit(df)

    secondsInDay = 86400

    future = model.make_future_dataframe(periods=secondsInDay)  # You can adjust the number of periods as needed
    forecast = model.predict(future)
    # Plot the forecast
    fig = model.plot(forecast)
    plt.show()
