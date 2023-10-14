if __name__ == "__main__":
    from utilities import *
    df = ugr_load_data("june", 2)

    # Crop 3 days starting from the second day
    df = ugr_get_first_n_days(df, 4)
    df = ugr_get_last_n_days(df, 3)

    # El algoritmo no va...
    period = ugr_detect_periodicity_sf(df, 86400, 3000)

    print(period)