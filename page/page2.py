import dash_bootstrap_components as dbc
import dash_html_components as html

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
        html.Div(id="prediction-graph")
    ],
    fluid=True
)
