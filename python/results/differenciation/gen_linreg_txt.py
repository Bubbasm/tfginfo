if __name__ == "__main__":
    from utilities import *
    import pandas as pd

    df1 = ugr_load_data("june", 2)
    df2 = ugr_load_data("june", 3)
    df = ugr_concat_data_list([df1, df2])
    df = ugr_crop_few_minutes(df, 10, 10)

    predict = 3 # minutes
    winlen = 15 # minutes

    file = open("linregr.txt", "w")

    print(len(df)/60)
    avgNoAttackMean = []
    avgNoAttackStd = []
    avgAttackMean = []
    avgAttackStd = []
    for win in range(0, len(df)//60-winlen, 1):
        dff = ugr_get_few_minutes(df, win, winlen)
        t = [i for i in range(len(dff))]
        # dff["Bitrate"][-(predict-1)*60:] = dff["Bitrate"][-(predict-1)*60:] + [i*10**6/2 for i in range((predict-1)*60)]

        # x_t = dff["Bitrate"].diff().dropna().reset_index(drop=True, inplace=False)
        x_t = pd.Series([-1/2*dff["Bitrate"][i-1] + 1/2*dff["Bitrate"][i+1] for i in range(1, len(dff)-1)])
        x_t_orig = x_t[:(winlen-predict)*60]

        a,b = x_t_orig.mean(), x_t_orig.std()

        # normalize x_t_new based on x_t_orig. If there is no attack, x_t_new should be similar to x_t_orig
        x_t_new = pd.Series([(x_t[i] - a)/b for i in range((winlen-predict)*60, len(x_t))])
        c,d = x_t_new.mean(), x_t_new.std()
        e,f = x_t.mean(), x_t.std()
        avgNoAttackMean.append(c)
        avgNoAttackStd.append(d)

        file.write(str(a) + " " + str(b) + " " + str(c) + " " + str(d) + " " + str(e) + " " + str(f) + " 0" + "\n")

        dff["Bitrate"][-(predict)*60:] = dff["Bitrate"][-(predict)*60:] + [i*10**6 for i in range((predict)*60)]

        # linregr0.txt: dff["Bitrate"][-(predict-2)*60:] = dff["Bitrate"][-(predict-2)*60:] + 1*10**8/2
        # linregr1.txt: dff["Bitrate"][-(predict-2)*60:] = dff["Bitrate"][-(predict-2)*60:] + 1*10**8
        # linregr2.txt: dff["Bitrate"][-(predict-1)*60:] = dff["Bitrate"][-(predict-1)*60:] + [i*10**6/2 for i in range((predict-1)*60)]
        # linregr3.txt: dff["Bitrate"][-(predict-1)*60:] = dff["Bitrate"][-(predict-1)*60:] + [i*10**6 for i in range((predict-1)*60)]
        # linregr4.txt: dff["Bitrate"][-(predict)*60:] = dff["Bitrate"][-(predict)*60:] + [i*10**6 for i in range((predict)*60)]
        # x_t = dff["Bitrate"].diff().dropna().reset_index(drop=True, inplace=False)
        x_t = pd.Series([-1/2*dff["Bitrate"][i-1] + 1/2*dff["Bitrate"][i+1] for i in range(1, len(dff)-1)])

        x_t_new = pd.Series([(x_t[i] - a)/b for i in range((winlen-predict)*60, len(x_t))])

        c,d = x_t_new.mean(), x_t_new.std()
        e,f = x_t.mean(), x_t.std()
        avgAttackMean.append(c)
        avgAttackStd.append(d)


        file.write(str(a) + " " + str(b) + " " + str(c) + " " + str(d) + " " + str(e) + " " + str(f) + " 1" + "\n")
    print(sum(avgNoAttackMean)/len(avgNoAttackMean), sum(avgNoAttackStd)/len(avgNoAttackStd))
    print(sum(avgAttackMean)/len(avgAttackMean), sum(avgAttackStd)/len(avgAttackStd))