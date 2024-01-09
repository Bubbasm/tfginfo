if __name__ == "__main__":
    from utilities import *
    import numpy as np
    from statsmodels.tsa.stattools import adfuller

    df1 = ugr_load_data("june", 2)
    df2 = ugr_load_data("june", 3)
    df = ugr_concat_data_list([df1, df2])
    df = ugr_crop_few_minutes(df, 10, 10)
    
    winlen = 15 # minutes

    print(len(df)//60)
    for window in range(0, len(df)//60, winlen):
        # print(window)
        dff = ugr_get_few_minutes(df, window, winlen)

        t = [i for i in range(len(dff))]
        y_t = dff["Bitrate"][:len(t)]
        y_adf = adfuller(y_t)
        if y_adf[1] < 0.05:
            # print("Stationary")
            continue

        polynomialDegree = 6
        polyn = np.polyfit(t, y_t, polynomialDegree)
        x_t = dff["Bitrate"]-np.polyval(polyn, t)
        x_adf = adfuller(x_t)
        if x_adf[1] > 0.05:
            print(window)

            print("Not stationary with polin")
            print(x_adf)
            print(y_adf)


# El adf test pasa para todas las ventanas con un p-valor menor que 0.05, con ventanas de 6 día
# El adf test pasa para todas las ventanas con un p-valor menor que 0.05, con ventanas de 2 día
# El adf test pasa para todas las ventanas con un p-valor menor que 0.05, con ventanas de 1 día
# Con un polinomio de grado 4, el adf test pasa para todas las ventanas con un p-valor menor que 0.05, con ventanas de 3 horas
# Con un polinomio de grado 6, el adf test pasa para todas las ventanas con un p-valor menor que 0.05, con ventanas de 2 horas
# Con un polinomio de grado 8, el adf test pasa para todas las ventanas con un p-valor menor que 0.05, con ventanas de 1.25 horas
# Con un polinomio de grado 9, el adf test pasa para todas las ventanas con un p-valor menor que 0.05, con ventanas de 1 hora
# Con un polinomio de grado 7, el adf test pasa para todas las ventanas con un p-valor menor que 0.05, con ventanas de 45 minutos
# Con un polinomio de grado 8, el adf test pasa para todas las ventanas con un p-valor menor que 0.05, con ventanas de 30 minutos
# Con un polinomio de grado 6, el adf test pasa para todas las ventanas con un p-valor menor que 0.05, con ventanas de 15 minutos

# Con un polinomio de grado 8, el adf test pasa para todas las ventanas con un p-valor menor que 0.01, con ventanas de 15 minutos