from random import uniform

silverUrl = 'https://api.nfusionsolutions.biz/api/v1/Metals/spot/history?token=c729d438-2c1b-46f6-9e5d-05ab9162dbcb&metals=silver&start=2009-01-01&interval='
stockList = ["silver"]
chartList = ["Scatter", "Candlestick"]
intervals = ["1mi", "30mi", "1h", "1d", "10d", "20d", "1m", "3m", "1y"]
prediction_interval = ["1d", "7d", "1m", "3m"]
# draft_graph = [uniform(0, 1) for x in range(1, 10)]

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

example_output = [0.9637154936790466, 3.8743019104003906e-07, 0.008967489004135132, 0.00017493963241577148,
                  3.9130449295043945e-05, 0.00010651350021362305, 0.038074642419815063, 0.00043573975563049316,
                  0.04264361783862114, 0.012469806708395481, 0.0010729571804404259, 0.10331336408853531]
