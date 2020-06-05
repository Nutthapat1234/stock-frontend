import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from config import path
from style import SIDEBAR_STYLE

component = html.Div(
    [
        html.H2("Stock", className="display-4"),
        html.Hr(),
        html.P(
            "Predict stock using Elliott Wave", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("real-time", href=path[0], id="real-time"),
                dbc.NavLink("prediction", href=path[1], id="prediction"),
                dbc.NavLink("back-test", href=path[2], id="back-test"),
                dbc.NavLink("stock-information", href=path[3], id="stock-information"),
                dbc.NavLink("about Elliot Wave", href=path[4], id="about"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)
