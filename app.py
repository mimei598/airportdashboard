import dash
from dash import Dash, html, dcc, dash_table, Input, Output
import pandas as pd

# Load your cleaned data (from earlier OpenSky script)
df = pd.read_csv("arrivals.csv")  # Replace with your actual filename

# Convert timestamp to readable format if needed
df['arrival_time'] = pd.to_datetime(df['arrival_time'])

# Select basic columns to show
display_columns = ['arrival_time', 'callsign', 'origin', 'icao24']

app = Dash(__name__)

app.layout = html.Div([
    html.H1("LSZH Arrivals Dashboard", style={'textAlign': 'center'}),
    
    dash_table.DataTable(
        id='arrivals-table',
        columns=[{'name': col.replace('_', ' ').title(), 'id': col} for col in display_columns],
        data=df[display_columns].to_dict('records'),
        page_size=10,
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'left', 'padding': '5px'},
    )
])

if __name__ == '__main__':
    app.run(debug=True)