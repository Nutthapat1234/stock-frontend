import dash_bootstrap_components as dbc
import dash_html_components as html

from config import intervals

tabList = []
for i in intervals:
    tabList.append(
        dbc.Tab(label=i, tab_id=i)
    )

component = dbc.Container(
    [
        dbc.Tabs(
            tabList,
            id="tabs",
            active_tab="1mi"
        ),
        html.Div(id="tab-content", className="p-4"),
    ]
)

