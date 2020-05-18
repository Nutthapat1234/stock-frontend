import dash_bootstrap_components as dbc
import dash_core_components as dcc


def generateControl(properties: list):
    forms = []
    for i in range(len(properties)):
        item = properties[i]
        forms.append(
            dbc.FormGroup(
                [
                    dbc.Label(item["name"]),
                    dcc.Dropdown(
                        id=item["id"],
                        options=[
                            {"label": col, "value": col} for col in item["columns"]
                        ],
                        value=item["value"],
                    ),
                ]
            )
        )
    controls = dbc.Card(
        forms,
        body=True,
    )

    return controls
