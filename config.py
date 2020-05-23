from random import uniform

silverUrl = 'https://api.nfusionsolutions.biz/api/v1/Metals/spot/history?token=c729d438-2c1b-46f6-9e5d-05ab9162dbcb&metals=silver&start=2009-01-01&interval='
predictionUrl = 'https://stormy-retreat-35286.herokuapp.com/model'
stockList = ["silver"]
chartList = ["Scatter", "Candlestick"]
intervals = ["1mi", "30mi", "1h", "1d", "10d", "20d", "1m", "3m", "1y"]
prediction_interval = ["1d", "10d", "1m", "3m"]
focus_range = {"1d": 2, "10d": 14, "1m": 120, "3m": 120}

standard_pattern = [[1.0, 0.32, 0.58, 0.0, 0.42, 0.21, 0.84, 0.32, 0.58, 0.16],
                    [0.0, 0.68, 0.42, 1.0, 0.58, 0.79, 0.16, 0.68, 0.42, 0.84],
                    [0.0, 0.46, 1.0, 0.15, 0.85, 0.31, 0.69, 0.38, 0.62, 0.42],
                    [0.0, 0.33, 0.17, 0.67, 0.5, 1.0, 0.5, 0.75, 0.42, 0.67],
                    [0.0, 0.63, 0.5, 1.0, 0.63, 0.75, 0.38, 0.63, 0.5, 1.0],
                    [0.0, 0.39, 0.13, 0.58, 0.45, 0.74, 0.61, 0.87, 0.71, 1.0],
                    [1.0, 0.71, 0.87, 0.61, 0.74, 0.45, 0.58, 0.13, 0.39, 0.0],
                    [0.0, 0.31, 0.1, 0.42, 0.35, 0.58, 0.48, 0.69, 0.56, 1.0],
                    [1.0, 0.56, 0.69, 0.48, 0.58, 0.35, 0.42, 0.1, 0.31, 0.0],
                    [0.0, 0.24, 0.12, 0.36, 0.24, 0.48, 0.33, 0.83, 0.64, 1.0],
                    [1.0, 0.64, 0.83, 0.33, 0.48, 0.24, 0.36, 0.12, 0.24, 0.0],
                    [0.0, 0.38, 0.19, 0.51, 0.83, 0.54, 1.0, 0.71, 0.9, 0.64]]

show_prediction = [
    [True, True, False, False, False, False, False, False, False, False, False, False, False, False],
    [True, True, True, False, False, False, False, False, False, False, False, False, False, False],
    [True, True, False, True, False, False, False, False, False, False, False, False, False, False],
    [True, True, False, False, True, False, False, False, False, False, False, False, False, False],
    [True, True, False, False, False, True, False, False, False, False, False, False, False, False],
    [True, True, False, False, False, False, True, False, False, False, False, False, False, False],
    [True, True, False, False, False, False, False, True, False, False, False, False, False, False],
    [True, True, False, False, False, False, False, False, True, False, False, False, False, False],
    [True, True, False, False, False, False, False, False, False, True, False, False, False, False],
    [True, True, False, False, False, False, False, False, False, False, True, False, False, False],
    [True, True, False, False, False, False, False, False, False, False, False, True, False, False],
    [True, True, False, False, False, False, False, False, False, False, False, False, True, False],
    [True, True, False, False, False, False, False, False, False, False, False, False, False, True],
]
