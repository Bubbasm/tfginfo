if __name__ == "__main__":
    import pandas as pd
    from pmdarima import auto_arima
      
    # Ignore harmless warnings
    import warnings
    warnings.filterwarnings("ignore")


    columns = ["Date", "Bitrate", "Packet rate"]
    df = pd.read_csv(r'../../datasets/ugr16/june_week2_csv/BPSyPPS.txt', sep=',', names=columns)
    df["Date"] = pd.to_datetime(df["Date"], unit='s')

    df = df[df["Date"] < df["Date"][0] + pd.Timedelta(days=3)]
    df = df[df["Date"][0] + pd.Timedelta(days=1) < df["Date"]]
    df.sort_index(inplace=True)
      
    # Fit auto_arima function to AirPassengers dataset
    stepwise_fit = auto_arima(df['Bitrate'], start_p = 1, start_q = 1,
                              max_p = 3, max_q = 3, m = 86400,
                              start_P = 0, seasonal = True,
                              d = None, D = 1, trace = True,
                              error_action ='ignore',   # we don't want to know if an order does not work
                              suppress_warnings = True,  # we don't want convergence warnings
                              stepwise = True)           # set to stepwise
      
    # To print the summary
    print(stepwise_fit.summary())

