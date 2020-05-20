from random import uniform

from dash.dependencies import Input, Output
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from app import app
import plotly.graph_objs as go
import component.intervalTab
from config import prediction_interval, show_prediction, example_output

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
        result = service.getGraph(stock, active_tab, chartType)
        figure = None
        if chartType == "Scatter":
            figure = go.Scatter(x=result["x"], y=result["y"], mode=result["mode"])
        elif chartType == "Candlestick":
            figure = go.Candlestick(x=result["start"],
                                    open=result["open"],
                                    high=result["high"],
                                    low=result["low"],
                                    close=result["close"])

        return dcc.Graph(figure=go.Figure(
            data=[figure],
            layout=go.Layout(
                height=600,
                # yaxis={'range': [min(y[-20:]), max(y[-20:])]},
                xaxis={
                    # 'range': [min(x[-20:]), max(x[-20:])],
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

        # for interval in prediction_interval:
        result = Service.getInstance().getGraph(stock, "1m", "Scatter")
        x = result["x"]
        y = result["y"]

        all_point = go.Scatter(x=x, y=y, mode=result["mode"])
        last_ten = go.Scatter(x=x[-10:], y=y[-10:], mode=result["mode"], name="last 10 point")
        container.append(html.H3("Prediction " + stock + " for " + "1m"))

        buttons = []
        data = []
        number = 0
        active = 0
        # for example
        possible_value = max(example_output)
        max_value = possible_value
        min_value = min(example_output)
        for index in range(13):
            show = False
            if index == 0:
                name = "original"
                data = [all_point, last_ten]
            else:
                if number < len(example_output) and example_output[number] == possible_value:
                    active = number + 1
                    show = True
                name = "pattern " + str(index) + " " + str(round(example_output[number] * 100)) + "%"
                label_name = "pattern " + str(index)
                data.append(
                    go.Scatter(x=x[-10:], y=[uniform(15, 20) for x in range(1, 10)], mode="lines+markers", name=label_name,
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
                height=600,
                width=1050,
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


def to_percentage(max_scale, min_scale, max_value, min_value, data):
    max_scale = max_scale
    min_scale = min_scale

    value = min_scale + ((data - min_value) * (max_scale - min_scale)) / (max_value - min_value)

    return value
