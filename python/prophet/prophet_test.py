if __name__ == "__main__":
    import pandas as pd
    from prophet import Prophet
    import matplotlib.pyplot as plt
    from utilities import *

    df = ugr_load_data("june", 2)

    # Assuming df is your DataFrame
    # Rename columns to meet Prophet's requirements
    df.rename(columns={'Date': 'ds', 'Bitrate': 'y'}, inplace=True)

    # Assuming you want to forecast Bitrate
    # You can create a Prophet model
    model = Prophet()

    # Fit the model with your data
    model.fit(df)

    secondsInDay = 86400

    # Create a DataFrame with future dates for prediction
    future = model.make_future_dataframe(periods=secondsInDay)  # You can adjust the number of periods as needed

    # Generate forecasts
    forecast = model.predict(future)

    # Plot the forecast
    fig = model.plot(forecast)
    plt.show()
