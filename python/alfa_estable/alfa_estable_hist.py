if __name__ == "__main__":
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    from scipy.stats import levy_stable
    from alfa_estable import *
    from utilities import *


    # Your calculated alpha, beta, gamma, and delta values
    # june_residue_mul
    df = residue_load_data("june_residue_mul")
    alpha, beta, gamma, delta = 1.8, 0.1, 0.085, 1.01

    # june_residue_mul_2seasons
    # df = residue_load_data("june_residue_mul_2seasons")
    # alpha, beta, gamma, delta = 1.75, -0.1, 0.081, 1

    # Function to generate Levy-stable distributed values
    def levy_stable_samples(alpha, beta, gamma, delta, size):
        return levy_stable.rvs(alpha, beta, loc=delta, scale=gamma, size=size)

    # Generate Levy-stable distributed samples
    levy_stable_data = levy_stable_samples(alpha, beta, gamma, delta, len(df))

    # Plot PDFs for original data and Levy-stable distribution
    plt.figure(figsize=(16, 9))

    ventana = ugr_crop_few_minutes(df, 15*4, 0)
    ventana = ventana[ventana["Date"] < ventana["Date"][0] + pd.Timedelta(seconds=15*60)]
    ventana.reset_index(drop=True, inplace=True)

    # ventana = df

    # Original Data
    plt.hist(ventana['Residue'], bins=200, density=True, alpha=0.5, range=(0,2), label='Original Data')
    print("Min: ", min(ventana['Residue']), "Max: ", max(ventana['Residue']))
    print("Mean: ", np.mean(ventana['Residue']), "Std: ", np.std(ventana['Residue']))

    # Levy-stable Distribution
    plt.hist(levy_stable_data, bins=500, density=True, alpha=0.5, range=(0,2), label='Levy-stable Distribution')

    # Alpha-stable Distribution
    # from pystable import *
    # st = StableVar(pn_ST,alpha=alpha, beta=beta, sigma=gamma, mu=delta)
    # x = rstable(len(df),st)
    # plt.hist(x, bins=500, density=True, alpha=0.5, range=(0,2), label='Alpha-stable Distribution')


    plt.title('Comparison of Original Data and Levy-stable Distribution')
    plt.xlabel('Value')
    plt.ylabel('Probability Density')
    plt.legend()
    plt.show()