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
                "silver": config.silverUrl
            }
            Service.__instance = self

    def __getHistory(self, name, interval):
        response = requests.get(self.baseUrl[name] + interval)
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
            response["high"].append(element["high"])
            response["low"].append(element["low"])
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

# if __name__ == '__main__':
#     graph = Service.getInstance().getGraph("silver", "1m", "waterfall")
#     for i in graph["y"]:
#         print(i)
