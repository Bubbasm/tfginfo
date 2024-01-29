if __name__ == "__main__":
    from utilities import *
    import matplotlib.pyplot as plt
    import skfda
    from sklearn.model_selection import GridSearchCV, train_test_split
    from skfda.ml.regression import FPCARegression
    from skfda.representation.grid import FDataGrid
    import numpy as np

    df0 = ugr_load_data("june", 1)
    df1 = ugr_load_data("june", 2)
    df2 = ugr_load_data("june", 3)
    df = ugr_concat_data_list([df0, df1, df2])
    df = ugr_crop_few_minutes(df, 60)
    dataComplete = ugr_get_first_n_days(df, 18)
    dataTrain = ugr_get_first_n_days(dataComplete, 7)

    secsInDay = 86400
    mergedSecs = 30
    dataTrainMerge = ugr_group_n_points(dataComplete,mergedSecs)
    pointsInDay = int(secsInDay/mergedSecs)
    data_matrix = [dataTrainMerge["Bitrate"][i:i+pointsInDay] for i in range(0, len(dataTrainMerge), pointsInDay)] 
    grid_points = range(pointsInDay)  # Grid points of the curves

    print(len(data_matrix), len(data_matrix[0]))

    X = skfda.FDataGrid(
        data_matrix=data_matrix,
        grid_points=grid_points,
    )
    y = range(len(data_matrix))

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=1,
    )

    reg = FPCARegression(n_components=5)
    reg.fit(X_train, y_train)
    test_score = reg.score(X_test, y_test)
    print(f"Score with n_components components: {test_score:.4f}")

    # param_grid = {"n_components": range(1, 28, 1)}
    # reg = FPCARegression()

    # # Perform grid search with cross-validation
    # gscv = GridSearchCV(reg, param_grid, cv=5)
    # gscv.fit(X_train, y_train)


    # print("Best params:", gscv.best_params_)
    # print(f"Best cross-validation score: {gscv.best_score_:.4f}")

    # secsInDay = 86400
    # mergedSecs = 30
    # dataTrainMerge = ugr_group_n_points(dataComplete,mergedSecs)
    # print(len(dataTrainMerge))
    # pointsInDay = int(secsInDay/mergedSecs)
    # grid_points = range(pointsInDay)  # Grid points of the curves
    # data_matrix = [dataTrainMerge["Bitrate"][i:i+pointsInDay] for i in range(0, len(dataTrainMerge), pointsInDay)] 
    # fd = skfda.FDataGrid(
    #     data_matrix=data_matrix,
    #     grid_points=grid_points,
    # )
    # fd.plot()
    # plt.show()
