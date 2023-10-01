def double_exponential_smoothing(series, alpha, beta):
    result = [series[0]]
    for n in range(1, len(series)+1):
        if n == 1:
            level, trend = series[0], series[1] - series[0]
        if n >= len(series): # we are forecasting
          value = result[-1]
        else:
          value = series[n]
        last_level, level = level, alpha*value + (1-alpha)*(level+trend)
        trend = beta*(level-last_level) + (1-beta)*trend
        result.append(level+trend)
    return result

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    xaxis = [0,1,2,3,4,5,6]
    series = [3,10,12,13,12,10,12]
    res = double_exponential_smoothing(series, alpha=0.9, beta=0.9)
    len(res)
    print(series,res)
    plt.plot(xaxis, series, "r--", xaxis, res[0:7], "b", [6,7], res[6:8], "go--")
    plt.show()
