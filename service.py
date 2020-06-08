import config
import requests


class Service:
    __instance = None

    @staticmethod
    def getInstance():
        if Service.__instance is None:
            Service()
        return Service.__instance

    def __init__(self):
        if Service.__instance is not None:
            raise Exception("The Service is already init")
        else:
            self.baseUrl = {
                "stock": config.stockUrl,
                "predictionUrl": config.predictionUrl,
                "backTestUrl": config.backtestUrl
            }
            Service.__instance = self

    def __getHistory(self, name, interval):
        response = requests.get(self.baseUrl['stock'] + name + '?timeframe=' + interval + '&range=all')
        if response.status_code == 200:
            data = response.json()[0]
            return data["data"]

    def __getScatter(self, name, interval):
        data = self.__getHistory(name, interval)
        x = []
        y = []
        for element in data["intervals"]:
            x.append(element["start"])
            y.append(element["last"])
        return {"x": x, "y": y, "size": len(y)}

    def __getCandlestick(self, name, interval):
        data = self.__getHistory(name, interval)
        response = {"start": [], "open": [], "high": [], "low": [], "close": []}
        for element in data["intervals"]:
            response["start"].append(element["start"])
            response["open"].append(element["open"])
            response["high"].append(element["high"] if 'high' in element else None)
            response["low"].append(element["low"] if 'low' in element else None)
            response["close"].append(element["last"])
        return response

    def getGraph(self, name: str, interval: str, chartType: str):
        response = {}
        if chartType.lower() == "scatter":
            response = self.__getScatter(name, interval)
            response["mode"] = "lines+markers"

        elif chartType.lower() == "candlestick":
            response = self.__getCandlestick(name, interval)

        return response

    def getPrediction(self, stock, data):
        payload = {
            "name": stock,
            "input": data
        }
        response = requests.post(self.baseUrl["predictionUrl"],
                                 json=payload)
        response = [x * 100 for x in response.json()["output"]]
        return response

    def getBackTest(self, stock):
        response = requests.get(self.baseUrl["backTestUrl"] + stock)
        data = response.json()
        x = []
        y = []
        for element in data["data"]:
            x.append(element["start"])
            y.append(element["last"])
        return {"x": x, "y": y, "label": data["label"]}


if __name__ == '__main__':
    from datetime import datetime

    print(datetime.now())
    r = requests.get('https://stormy-mesa-57066.herokuapp.com/BDMS_BK?timeframe=1m&range=all')
    print(datetime.now())
