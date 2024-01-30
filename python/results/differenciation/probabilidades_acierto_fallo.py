# valores más grandes resultan en más falsos negativos a cambio de menos falsos positivos
# offset = 0.02
# offset = 0.017302779864763335
# offset = 0.016556434219985622
# offset = 0.015
from joblib import Parallel, delayed

def is_attack(m,s) -> bool:
    # otra posible comprobación es m>=offset para distintos valores de offset
    return (0.31+11*m-0.07*s)>=0.5 or m>=0.02

def task(winlen, predict, attackType, df):
    probs = [[0, 0],[0, 0]]
    win = random.randint(0, len(df)//60-winlen)

    dff = ugr_get_few_minutes(df, win, winlen)
    t = [i for i in range(len(dff))]

    x_t = dff["Bitrate"].diff().dropna().reset_index(drop=True, inplace=False)
    x_t_orig = x_t[:(winlen-predict)*60]

    a,b = x_t_orig.mean(), x_t_orig.std()

    x_t_new = pd.Series([(x_t[i] - a)/b for i in range((winlen-predict)*60, len(x_t))])
    m = x_t_new.mean()
    s = x_t_new.std()

    if is_attack(m,s):
        probs[0][1] += 1
    else:
        probs[0][0] += 1

    if attack["type"] == 0:
        dff["Bitrate"][-(predict-1)*60:] = dff["Bitrate"][-(predict-1)*60:] + 1*10**8/2
    elif attack["type"] == 1:
        dff["Bitrate"][-(predict-1)*60:] = dff["Bitrate"][-(predict-1)*60:] + [(i*10**6)/2 for i in range((predict-1)*60)]

    x_t = dff["Bitrate"].diff().dropna().reset_index(drop=True, inplace=False)
    x_t_new = pd.Series([(x_t[i] - a)/b for i in range((winlen-predict)*60, len(x_t))])
    m = x_t_new.mean()
    s = x_t_new.std()

    if is_attack(m,s):
        probs[1][1] += 1
    else:
        probs[1][0] += 1
    return probs

if __name__ == "__main__":
    from utilities import *
    import pandas as pd
    import random

    df1 = ugr_load_data("june", 2)
    df2 = ugr_load_data("june", 3)
    df = ugr_concat_data_list([df1, df2])
    df = ugr_crop_few_minutes(df, 10, 10)

    predict = 3
    winlen = 13
    attack = {"name": "constante", "type": 0}
    # attack = {"name": "creciente", "type": 1}

    nobs = 5000

    results = Parallel(n_jobs=4)(delayed(task)(winlen, predict, attack['type'], df) for i in range(nobs))
    probs = [[0, 0],[0, 0]]
    for i in range(len(results)):
        probs[0][0] += results[i][0][0]
        probs[0][1] += results[i][0][1]
        probs[1][0] += results[i][1][0]
        probs[1][1] += results[i][1][1]

    etiquetas1 = ["-","PredNA", " PredA"]
    etiquetas2 = ["-","RealNA", "RealA"]
    print(f"Prueba ejecutada con {nobs} observaciones")
    print(f"Tamaño de ventana de {winlen} minutos")
    print(f"Ataque con tráfico {attack['name']}")
    print("Probabilidades de acierto y fallo:")
    print('\n'.join(['\t'.join(etiquetas1)]+[etiquetas2[i+1]+"\t"+'\t'.join(['{:5.2f}%'.format(100*probs[i][j]/nobs) for j in range(2)]) for i in range(2)]))