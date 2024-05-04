import numpy as np
from math import *
from scipy.io import savemat
from random import *
import time
from datetime import datetime, timedelta
from holt_winters import *
import logging, sys
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

NO = 0
SI = 1
DEBUG=1

#------------------------------------------------------------------------------------------------------------
#
#  Holt-Winters: El algoritmo Holt-Winters también conocido como suavizado exponencial triple es um método
#                para pronosticar un número de puntos de una serie estacional teniendo en cuenta la duración 
#                de la temporada, la tendencia y el nivel. Su mayor ventaja frente al suavizado exponencial
#                simple y doble es que este método nos permite pronosticar muchos más puntos que estos dos 
#                métodos.
#
#------------------------------------------------------------------------------------------------------------                                               
if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from datetime import datetime
    import matplotlib.dates as mdates
    import pandas as pd
    from utilities import *
    import matplotlib.dates as mdates
    
    df1 = ugr_load_data("june", 2)
    df2 = ugr_load_data("june", 3)

    df = ugr_concat_data_list([df1, df2])
    df = ugr_crop_few_minutes(df, 10)

    train = ugr_get_first_n_days(df, 10)
    train = ugr_crop_few_minutes(train, 0, 23*60)
    test = ugr_get_first_n_days(df, 11)
    test = ugr_crop_few_minutes(test, 0, 23*60)

    #Definición de parámetros para la predicción
    segsInDay = 86400
    slen = segsInDay
    n_preds = segsInDay
    numero_de_periodos=20
    precision=int(1e2)

    param="Bitrate"
    series=train[param].tolist()
    valores=test[param][-n_preds:].tolist()
    alpha_definitivo, beta_definitivo, gamma_definitivo = 0.9, 0.0, 0.9
    diferencia_minima = 1.975e15
    segsInDay = 86400
    movingAvgWindow = 60*10
    t0 = time.time()
    while True:
        ###Creamos un array del tamaño de la serie que queremos pasar para calcular la predicción
        ##Carga de los datos para la predicción: La predicción se hace a partir del principio de la segunda ventana
        #Es necesario desplazar el inicio de la ventana en funcion del periodo que estamos calculando
        ##Busqueda de los valores optimos de alpha beta y gamma
        diferencia_actual = diferencia_minima
        menor_diferencia = diferencia_actual
        for T in np.linspace(1000,0,precision):
            #Generación de un punto aleatorio 
            alpha = random()
            beta = 0.0
            gamma = random()
            result = triple_exponential_smoothing(series, slen, alpha, beta, gamma, n_preds)

            #Nos quedamos con los datos del período predicho
            prediccion=np.array(np.array(result[-n_preds:]))
            #Calculamos la distancia entre los valores reales y los predichos
            distancia=np.mean(((prediccion-valores)**2))
    
            # Si el error es menor, nos quedamos con el nuevo punto
            if( (distancia<diferencia_actual) or
            # Si el error es mayor con probabilidad cada vez menor se elige el nuevo punto para
            # evitar mínimos locales
            ( (distancia>diferencia_actual)and (exp((T-1000)/100) > random()) )   ):
                diferencia_actual=distancia
                alpha_actual=alpha
                beta_actual=beta
                gamma_actual=gamma
                if diferencia_actual < menor_diferencia :
                    logging.debug("Encontrado nuevo mínimo")
                    menor_diferencia = diferencia_actual
                    diferencia_minima = min(diferencia_actual, diferencia_minima)
                    alpha_definitivo = alpha_actual
                    beta_definitivo = beta_actual
                    gamma_definitivo = gamma_actual 
                    with open("simmulatedAnnealing.txt", "a") as file1:
                        file1.write(f"alpha, beta, gamma= {alpha_definitivo}, {beta_definitivo}, {gamma_definitivo}  , Distancia = {menor_diferencia:.3E}\n")
                    fig, axs = plt.subplots(2, 1, figsize=(16,8))
                    plt.subplots_adjust(left=0.1, bottom=0.1)
                    
                    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y %H:%M:%S'))
                    plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
                    plt.gcf().autofmt_xdate()

                    fig.suptitle(f"Holt-Winters, alpha={alpha}, beta={beta}, gamma={gamma}")
                    fig.supxlabel("Time")
                    fig.supylabel("Value")

                    line1, = axs[0].plot(test["Date"][-segsInDay:], smooth(result, movingAvgWindow)[-segsInDay:], color="#1368CE", label="Prediction Holt-Winters")
                    line2, = axs[0].plot(test["Date"][-segsInDay:], smooth(test[param], movingAvgWindow)[-segsInDay:], color="#26890C", label="Real")
                    line3, = axs[1].plot(test["Date"][-segsInDay:], smooth(result-test[param], movingAvgWindow)[-segsInDay:], color="#E21B3C", label="Error")

                    print("MSE: ", "{:.2E}".format(np.mean(((result-test[param])[-segsInDay:])**2)))

                    axs[0].legend()
                    axs[1].legend()
                    plt.savefig("holt_winters_prediccion_three.svg")
                logging.debug("T = %2d D = %.3E"% (T, diferencia_actual))

        
    t1 = time.time()
    print("Tiempo ejecucion %5.2f segundos" % (t1-t0))


