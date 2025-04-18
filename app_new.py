import dash
from dash import Dash, html, dcc, dash_table, Input, Output
import pandas as pd
import fetch_data

app = Dash(__name__)
app.title = "LSZH Airport Live Arrivals"

app.layout = html.Div([
    html.H1("LSZH Live Arrivals"),
    dcc.Interval(
        id='interval-component',
        interval=20*1000,  # in milliseconds
        n_intervals=0  # starts at 0
    ),
    html.Div(id='live-update-table'),
])

@app.callback(
    Output('live-update-table', 'children'),
    Input('interval-component', 'n_intervals')
)

def update_table(n):
    df = fetch_data.fetch_aircraft_nearby()  

    table = html.Table([
        html.Thead(html.Tr([
            html.Th(col) for col in df.columns
        ])),
        html.Tbody([
            html.Tr([
                html.Td(df.iloc[i][col]) for col in df.columns
            ]) for i in range(len(df))
        ])
    ])
    return table

if __name__ == '__main__':
    app.run(debug=True)