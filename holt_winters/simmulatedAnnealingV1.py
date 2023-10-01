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

    columns = ["Date", "Bitrate", "Packet rate"]

    # df0 = pd.read_csv(r'../../datasets/ugr16/june_week1_csv/BPSyPPS.txt', sep=',', names=columns)
    df1 = pd.read_csv(r'../../datasets/ugr16/june_week2_csv/BPSyPPS.txt', sep=',', names=columns)
    df2 = pd.read_csv(r'../../datasets/ugr16/june_week3_csv/BPSyPPS.txt', sep=',', names=columns)
    df3 = pd.read_csv(r'../../datasets/ugr16/july_week1_csv/BPSyPPS.txt', sep=',', names=columns)
    df = pd.concat([df1, df2, df3], ignore_index=True)
    #Definición de parámetros para la predicción
    segsInDay = 86400
    valorventanaseg=segsInDay*5
    slen = segsInDay
    n_preds = segsInDay
    numero_de_periodos=20
    diferencia_minima=1.743e10
    precision=int(1e2)

    days_df = len(df) // segsInDay
    logging.info("Days in dataframe %d" % (days_df))
    t0 = time.time()
    periodo = 0
    series=df["Bitrate"][valorventanaseg+periodo*slen:2*valorventanaseg+periodo*slen].tolist()
    valores=df["Bitrate"][2*valorventanaseg+periodo*slen:2*valorventanaseg+periodo*slen+slen].tolist()
    alpha_definitivo, beta_definitivo, gamma_definitivo = 0.72149, 0.00004, 0.17637

    while True:
        logging.debug("Periodo: %d"% (periodo))      
        ###Creamos un array del tamaño de la serie que queremos pasar para calcular la predicción
        ##Carga de los datos para la predicción: La predicción se hace a partir del principio de la segunda ventana
        #Es necesario desplazar el inicio de la ventana en funcion del periodo que estamos calculando
        ##Busqueda de los valores optimos de alpha beta y gamma
        diferencia_actual = diferencia_minima
        menor_diferencia = diferencia_actual
        for T in np.linspace(1000,0,precision):
            #Generación de un punto aleatorio 
            alpha = random()
            beta = random()
            gamma = random()
            result = triple_exponential_smoothing(series, slen, alpha, beta, gamma, n_preds)

            #Nos quedamos  con los datos del período predicho
            prediccion=np.array(np.array(result[valorventanaseg:]))
            #Calculamos la distancia entre los valores reales y los predichos
            distancia=np.sqrt(sum((prediccion-valores)**2))
            
    
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
                logging.debug("T = %2d D = %.3E"% (T, diferencia_actual))
            

            
        logging.debug("Periodo %d -  alpha, beta, gamma= %2.5f, %2.5f, %2.5f  , Distancia = %.3E"%
                            (periodo, alpha_definitivo, beta_definitivo, gamma_definitivo, menor_diferencia))

        
    t1 = time.time()
    print("Tiempo ejecucion %5.2f segundos" % (t1-t0))


