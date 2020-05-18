import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from style import SIDEBAR_STYLE

component = html.Div(
    [
        html.H2("Stock", className="display-4"),
        html.Hr(),
        html.P(
            "Predicate stock using Elliott Wave", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("real-time", href="/page-1", id="page-1-link"),
                dbc.NavLink("predicate", href="/page-2", id="page-2-link"),
                dbc.NavLink("information", href="/page-3", id="page-3-link"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)
