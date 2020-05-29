from datetime import datetime, timedelta
from random import uniform, randint

import pathlib
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from app import app, cache
import plotly.graph_objs as go
import component.intervalTab
from config import prediction_interval, show_prediction, standard_pattern, focus_range

from page import realTime, prediction, backTest
from service import Service

TIMEOUT = 60 * 60
prediction_status = None


@app.callback(
    [Output(f"page-{i}-link", "active") for i in range(1, 6)],
    [Input("url", "pathname")],
)
def toggle_active_links(pathname):
    if pathname == "/":
        # Treat page 1 as the homepage / index
        return True, False, False, False, False
    return [pathname == f"/page-{i}" for i in range(1, 6)]


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname in ["/", "/page-1"]:
        return realTime.component
    elif pathname == "/page-2":
        return prediction.component
    elif pathname == "/page-3":
        return backTest.component
    elif pathname == "/page-4":
        return html.P("Stock-information!")
    elif pathname == "/page-5":
        return html.P("About Elliott Wave!")
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


@app.callback(
    Output("tab-content", "children"),
    [Input("tabs", "active_tab"),
     Input("stock-variable", "value"),
     Input("chart-variable", "value"), ]
)
def render_real_time_tab_content(active_tab, stock, chartType):
    service = Service.getInstance()
    if stock and chartType:
        if active_tab in ["1mi","30mi","1h"] and chartType == "Candlestick":
            return
        result = service.getGraph(stock, active_tab, chartType)
        figure = None
        if chartType == "Scatter":
            figure = go.Scatter(x=result["x"], y=result["y"], mode="lines")
            focus = result["x"]
        elif chartType == "Candlestick":
            figure = go.Candlestick(x=result["start"],
                                    open=result["open"],
                                    high=result["high"],
                                    low=result["low"],
                                    close=result["close"])
            focus = result["start"]

        return dcc.Graph(figure=go.Figure(
            data=[figure],
            layout=go.Layout(
                height=600,
                xaxis={
                    # 'range': [min(focus[-20:]), max(focus[-20:])],
                    'rangeslider': {'visible': True},
                },
            ),
        ))
    else:
        return dcc.Graph(figure=go.Figure(
            data=[go.Scatter(x=[], y=[], mode="lines+markers")],
            layout=go.Layout(
                height=600
            )
        ))


@app.callback(
    Output("prediction-graph", "children"),
    [Input("stock-prediction-variable", "value")]
)
@cache.memoize(timeout=TIMEOUT)
def render_prediction_graph(stock):
    global prediction_status
    stock = stock or prediction_status
    if stock:
        container = []
        for interval in prediction_interval:
            result = Service.getInstance().getGraph(stock, interval, "Scatter")
            x = result["x"]
            y = result["y"]

            all_point = go.Scatter(x=x, y=y, mode="lines", showlegend=False)
            last_ten = go.Scatter(x=x[-10:], y=y[-10:], mode=result["mode"], name="last 10 point")
            container.append(html.H3("Prediction " + stock + " for " + interval))

            buttons = []
            data = []
            number = 0
            active = 0
            active_name = ""
            # for example
            output = Service.getInstance().getPrediction("XAUUSD", y[-10:])
            possible_value = max(output)
            for index in range(13):
                show = False
                if index == 0:
                    name = "original"
                    data = [all_point, last_ten]
                else:
                    name = "pattern " + str(index) + " " + str(round(output[number])) + "%"
                    if number < len(output) and output[number] == possible_value:
                        active_name = name
                        active = number + 1
                        show = True
                    label_name = "pattern " + str(index)
                    normalized_value = normalize(max(y[-10:]), min(y[-10:]), standard_pattern[number])
                    data.append(
                        go.Scatter(x=x[-10:], y=normalized_value, mode="lines+markers",
                                   name=label_name,
                                   visible=show)
                    )
                    number += 1
                buttons.append(dict(label=name,
                                    method="update",
                                    args=[{"visible": show_prediction[index]},
                                          {"title": name,
                                           "annotations": []}]), )

            fig = go.Figure(
                data=data,
                layout=go.Layout(
                    title=active_name,
                    height=600,
                    width=1050,
                    yaxis={
                        'range': [min(y[-20:]) - 5, max(y[-20:]) + 5]
                    },
                    xaxis={
                        'range': [datetime.fromisoformat(min(x[-15:])) - timedelta(days=focus_range[interval]),
                                  datetime.fromisoformat(max(x[-15:])) + timedelta(days=focus_range[interval])

                                  ],
                    }
                ),
            )
            fig.update_layout(
                updatemenus=[
                    dict(
                        type="buttons",
                        direction="down",
                        active=active,
                        x=1.4,
                        y=1.1,
                        buttons=list(buttons),
                    )
                ])

            container.append(
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dcc.Graph(figure=fig)
                            ]
                        ),
                    ],
                )
            )
        prediction_status = stock
        return container


@app.callback(Output("callback-temp", "children"), [Input('prediction-cache', 'n_intervals')])
def delete_cache(n):
    if n == 0:
        return
    cache.clear()


@app.callback(
    Output("backTest-graph", "children"),
    [Input("stock-backTest-variable", "value")]
)
def render_backTest_graph(stock):
    if stock:
        result = Service.getInstance().getBackTest("XAUUSD")
        x_value = result["x"]
        y_value = result["y"]
        data_set = {}
        graphs = []
        for element in result["label"]:
            if element["pattern"] not in data_set:
                data_set[element["pattern"]] = {"x_value": [], "y_value": [], "pattern": element["pattern"]}
            index = element["index"]
            start_index = -index - 9
            end_index = -index + 1
            if end_index == 0:
                end_index = len(y_value)
            data_set[element["pattern"]]["x_value"] += x_value[start_index:end_index]
            data_set[element["pattern"]]["x_value"] += [None]
            data_set[element["pattern"]]["y_value"] += y_value[start_index:end_index]
            data_set[element["pattern"]]["y_value"] += [None]

        for pattern in sorted(data_set):
            pattern = data_set[pattern]
            data = [go.Scatter(x=x_value, y=y_value, mode="lines", ),
                    go.Scatter(x=pattern["x_value"], y=pattern["y_value"], mode="lines+markers")]
            fig = go.Figure(data=data, layout=go.Layout(title="Pattern" + str(pattern["pattern"])))
            graphs.append(dcc.Graph(figure=fig))
        return graphs


def normalize(max_scale, min_scale, data):
    max_scale = max_scale
    min_scale = min_scale
    max_value = max(data)
    min_value = min(data)
    output = []
    for element in data:
        output.append(min_scale + ((element - min_value) * (max_scale - min_scale)) / (max_value - min_value))

    return output
