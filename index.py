import dash_core_components as dcc
import dash_html_components as html
from app import app
import callback
from component import sidebar
from style import CONTENT_STYLE

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar.component, content])

if __name__ == '__main__':
    app.run_server(debug=True)
