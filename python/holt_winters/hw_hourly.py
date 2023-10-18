if __name__ == "__main__":
    from utilities import *
    from statsmodels.tsa.api import ExponentialSmoothing, SimpleExpSmoothing, Holt

    df = ugr_load_data("may", 3)
    df = ugr_crop_few_minutes(df, 150, 2)
    df = ugr_get_first_n_days(df, 3)
    print(len(df))
    dfInput = ugr_get_first_n_days(df, 2)
    print(len(dfInput))

    param = "Bitrate"

    fitted_model = ExponentialSmoothing(dfInput[param],trend="mul",seasonal="mul",seasonal_periods=60*60).fit()
    test_predictions = fitted_model.forecast(3600)


    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(16,9))
    plt.plot(df["Date"][:len(dfInput)+3600], df[param][:len(dfInput)+3600], label="Bitrate")
    plt.plot(df["Date"][len(dfInput):len(dfInput)+3600], test_predictions, label="Forecast")

    plt.legend()
    plt.show()
