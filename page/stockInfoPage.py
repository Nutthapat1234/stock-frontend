import dash_html_components as html
import dash_bootstrap_components as dbc
from component.stockInfo import app_stockInfo

component = dbc.Container(
    [
        dbc.Row([
            dbc.Spinner(
                dbc.Container(
                    app_stockInfo.layout,
                    fluid=True,
                ),
                spinner_style={"width": "3rem", "height": "3rem"},
                color="primary"
            )
        ])
    ])
