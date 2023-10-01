def exponential_smoothing(series, alpha):
    result = [series[0]] # first value is same as series
    for n in range(1, len(series)):
        result.append(alpha * series[n] + (1 - alpha) * result[n-1])
    return result

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    xaxis = [0,1,2,3,4,5,6]
    series = [3,10,12,13,12,10,12]
    res = exponential_smoothing(series, 0.1)
    plt.plot(xaxis, series, "r--", xaxis, res)
    plt.show()
