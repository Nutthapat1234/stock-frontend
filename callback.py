from datetime import datetime, timedelta
from random import uniform

from dash.dependencies import Input, Output
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from app import app
import plotly.graph_objs as go
import component.intervalTab
from config import prediction_interval, show_prediction, standard_pattern, focus_range

from page import page1, page2
from service import Service


@app.callback(
    [Output(f"page-{i}-link", "active") for i in range(1, 4)],
    [Input("url", "pathname")],
)
def toggle_active_links(pathname):
    if pathname == "/":
        # Treat page 1 as the homepage / index
        return True, False, False
    return [pathname == f"/page-{i}" for i in range(1, 4)]


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname in ["/", "/page-1"]:
        return page1.component
    elif pathname == "/page-2":
        return page2.component
    elif pathname == "/page-3":
        return html.P("Oh cool, this is page 3!")
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
def render_tab_content(active_tab, stock, chartType):
    service = Service.getInstance()
    if stock and chartType:
        if active_tab == "1mi" and chartType == "Candlestick":
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
                    'range': [min(focus[-20:]), max(focus[-20:])],
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
def render_prediction_graph(stock):
    if stock:
        container = []

        for interval in prediction_interval:
            result = Service.getInstance().getGraph(stock, interval, "Scatter")
            x = result["x"]
            y = result["y"]

            all_point = go.Scatter(x=x, y=y, mode="lines")
            last_ten = go.Scatter(x=x[-10:], y=y[-10:], mode=result["mode"], name="last 10 point")
            container.append(html.H3("Prediction " + stock + " for " + interval))

            buttons = []
            data = []
            number = 0
            active = 0
            active_name = ""
            # for example
            output = Service.getInstance().getPrediction(y[-10:])
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
                        'range': [min(y[-20:]) - 1, max(y[-20:]) + 1]
                    },
                    xaxis={
                        'range': [datetime.fromisoformat(min(x[-20:])) - timedelta(days=focus_range[interval]),
                                  datetime.fromisoformat(max(x[-20:])) + timedelta(days=focus_range[interval])

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

        return dbc.Container(
            container,
            fluid=True
        )


def normalize(max_scale, min_scale, data):
    max_scale = max_scale
    min_scale = min_scale
    max_value = max(data)
    min_value = min(data)
    output = []
    for element in data:
        output.append(min_scale + ((element - min_value) * (max_scale - min_scale)) / (max_value - min_value))

    return output
