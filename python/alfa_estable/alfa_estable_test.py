if __name__ == "__main__":
    from utilities import *
    from alfa_estable import *

    df = residue_load_data("june_residue_mul")

    df = residue_get_first_n_days(df, 2)
    df = residue_get_last_n_days(df, 1)
    df = residue_crop_few_minutes(df, 60*9)


    print(residue_levy_fit(df))
