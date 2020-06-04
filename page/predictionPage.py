import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc

from component.control import generateControl
from config import stockList

component = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(generateControl(
                    [
                        {
                            "name": "stock",
                            "id": "stock-prediction-variable",
                            "columns": stockList,
                            "value": None
                        },
                    ]
                )),
            ]
        ),
        html.Br(),
        dbc.Spinner(
            dbc.Container(
                id="prediction-graph",
                fluid=True,
            ),
            spinner_style={"width": "3rem", "height": "3rem"},
            color="primary"
        ),
    ],
    fluid=True
)
