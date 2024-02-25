from joblib import Parallel, delayed
from diff_utils import *

# good for increasing attack
def is_attack(m,s) -> bool:
    return (-1.0+96.7263*m-0.2394*s)>0

# def is_attack(m,s) -> bool:
#     return (-1.77+137*m-0.24*s)>0

def simulate_test(df, win, winlen, predict, diffType, attackLen=2, attackType=None):
    dff = ugr_get_few_minutes(df, win, winlen)
    if attackType is not None:
        dff = apply_attack(dff, attackLen, attackType)
    t = [i for i in range(len(dff))]
    x_t = diff_series(dff, diffType)
    x_t_orig = x_t[:(winlen-predict)*60]
    a,b = x_t_orig.mean(), x_t_orig.std()
    x_t_new = pd.Series([(x_t[i] - a)/b for i in range((winlen-predict)*60, len(x_t))])
    m = x_t_new.mean()
    s = x_t_new.std()
    return is_attack(m,s)


def task(winlen, predict, attackType, diffType, df):

    def predict_alg(doAttack):
        prob = [0, 0]
        attack = attackType if doAttack else None
        results = [simulate_test(df, win+i, winlen, predict, diffType, i, attack) for i in range(1, 4)]
        if sum(results)>=2:
            prob[1] += 1
        else:
            prob[0] += 1
        
        return prob
    
    probs = [[0, 0],[0, 0]]
    win = random.randint(0, len(df)//60-winlen*2)
    
    # WITHOUT ATTACK
    probs[0] = predict_alg(False)

    # WITH ATTACK
    probs[1] = predict_alg(True)

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
    winlen = 15
    attack = {"name": "constant", "type": 0}
    attack = {"name": "increasing", "type": 1}
    differenciation = {"name": "first discrete diff.", "type": 0}
    differenciation = {"name": "convolution", "type": 1}

    nobs = 500

    results = Parallel(n_jobs=4)(delayed(task)(winlen, predict, attack['type'], differenciation['type'], df) for i in range(nobs))
    probs = [[0, 0],[0, 0]]
    for i in range(len(results)):
        probs[0][0] += results[i][0][0]
        probs[0][1] += results[i][0][1]
        probs[1][0] += results[i][1][0]
        probs[1][1] += results[i][1][1]

    etiquetas1 = ["-","PredNA", " PredA"]
    etiquetas2 = ["-","RealNA", "RealA"]
    print(f"Test executed with {nobs} observations")
    print(f"Window size of {winlen} minutes")
    print(f"Attack with {attack['name']} traffic")
    print(f"Differenciation with {attack['name']}")
    print("Probabilities of success and failure:")
    print('\n'.join(['\t'.join(etiquetas1)]+[etiquetas2[i+1]+"\t"+'\t'.join(['{:5.2f}%'.format(100*probs[i][j]/nobs) for j in range(2)]) for i in range(2)]))