from dash.dependencies import Input, Output
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from app import app
import plotly.graph_objs as go
import component.intervalTab

from page import page1
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
        return html.P("This is the content of page 2. Yay!")
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
