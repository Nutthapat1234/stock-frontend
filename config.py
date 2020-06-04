stockUrl = 'https://stormy-mesa-57066.herokuapp.com/'
predictionUrl = 'https://stormy-retreat-35286.herokuapp.com/model'
backtestUrl = 'https://stormy-retreat-35286.herokuapp.com/backtest/'
stockList = ['AAPL', 'FB', 'GOOGL', 'SBUX', 'MSFT', 'BDMS_BK', 'TRUE_BK', 'LPN_BK', 'WHA_BK', 'CPALL_BK']
path = ["/real-time", "/prediction", "/back-test", "/stock-information" ,"/about"]
chartList = ["Scatter", "Candlestick"]
intervals = ["1m", "30m", "1h", "1d", "1wk", "1mo", "3mo"]
except_interval = ["1m", "30m", "1h"]
prediction_interval = ["1d", "1wk", "1mo", "3mo"]
focus_range = {"1d": 2, "1wk": 14, "1mo": 120, "3mo": 120}
pattern_name = {1: "Correction Zigzag",
                2: "reverse Correction Zigzag",
                3: "Triangle pattern",
                4: "Triangle pattern",
                5: "Correction Zigzag weak b",
                6: "impulse wave 5 extension",
                7: "reverse impulse wave 1 extension",
                8: "impulse wave 3 extension",
                9: "reverse impulse wave 3 extension",
                10: "impulse wave 1 extension",
                11: "reverse impulse wave 5 extension",
                12: "complete cycle"}

standard_pattern = [[1.0, 0.32, 0.58, 0.0, 0.42, 0.21, 0.84, 0.32, 0.58, 0.16],
                    [0.0, 0.68, 0.42, 1.0, 0.58, 0.79, 0.16, 0.68, 0.42, 0.84],
                    [0.0, 0.46, 1.0, 0.15, 0.85, 0.31, 0.69, 0.38, 0.62, 0.42],
                    [0.36, 0.5, 0.25, 0.57, 0.20, 0.71, 0.10, 1.0, 0.46, 0],
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

predict_trend = {"up": [1, 3, 4, 7, 9, 11, 12], "down": [2, 5, 6, 8, 10]}
