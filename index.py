import dash_core_components as dcc
import dash_html_components as html
from app import app, server
import callback
from component import sidebar
from style import CONTENT_STYLE

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar.component, content,
                       html.Div(hidden=True, id="callback-temp"),
                       dcc.Interval(
                           id='prediction-cache',
                           interval=12 * 60 * 60 * 1000,  # in milliseconds
                           max_intervals=-1,
                           n_intervals=0
                       )])

if __name__ == '__main__':
    # app.run_server(host='0.0.0.0', debug=True)
    app.run_server()
