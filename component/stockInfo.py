import dash
import pandas as pd
from app import app
import dash_html_components as html
import dash_core_components as dcc

app_stockInfo = dash.Dash(__name__)
df = pd.read_csv('./assets/APPLEINC1.csv')
df2 = pd.read_csv('./assets/APPLEINC2.csv')

app_stockInfo.layout = html.Div([
    html.Div([
        dcc.Dropdown(
            id='stock_dropdown', style={'height': '40px', 'width': '1090px'},
            options=[
                {'label': 'AAPL', 'value': 'AAPL'},
                {'label': 'FB', 'value': 'FB'},
                {'label': 'GOOGL', 'value': 'GOOGL'},
                {'label': 'SBUX', 'value': 'SBUX'},
                {'label': 'MSFT', 'value': 'MSFT'},
                {'label': 'BDMS', 'value': 'BDMS_BK'},
                {'label': 'TRUE', 'value': 'TRUE_BK'},
                {'label': 'LPN', 'value': 'LPN_BK'},
                {'label': 'WHA', 'value': 'WHA_BK'},
                {'label': 'CPALL', 'value': 'CPALL_BK'},
            ],
            placeholder="Select a Stock",
        ),
        html.Br(),
        html.Img(id="image", style={'height': '20%', 'width': '50%', 'textAlign': 'center', 'margin-left': 'auto',
                                    'margin-right': 'auto', 'display': 'block'}),
        html.Br(),
        html.Div(id='dd-output-container'),
        html.Br(),
    ]),
    html.Div(
        id='income_table'
    ),
    html.Div(
        id='stakeholder_table'
    )
])
