import dash_bootstrap_components as dbc
from component import intervalTab
from component.control import generateControl
from config import stockList, chartList

component = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(generateControl(
                    [
                        {
                            "name": "stock",
                            "id": "stock-variable",
                            "columns": stockList,
                            "value": None
                        },
                    ]
                ), md=5),
                dbc.Col(generateControl(
                    [
                        {
                            "name": "chart Type",
                            "id": "chart-variable",
                            "columns": chartList,
                            "value": None
                        }
                    ]
                ), md=5),
            ],
            align="center",
        ),
        dbc.Row(
            [
                dbc.Col(
                     intervalTab.component,
                )
            ]
        )
    ],
    fluid=True,
)
