from flask import Flask, render_template
import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px

# Flask app
server = Flask(__name__)

# Dash app
app = dash.Dash(__name__, server=server, url_base_pathname='/dashboard/')

# Load dataset
data = pd.read_csv('boston.csv', index_col=0)

# Create figures
house_price_fig = px.histogram(
    data, x="PRICE", nbins=20, title="House Price Distribution",
    labels={"PRICE": "Price (in 000s)"},
    template="plotly_white",
    color_discrete_sequence=["red"]
)

house_distance_fig = px.histogram(
    data, x="DIS", nbins=50, title="Distance to Employment Centers",
    labels={"DIS": "Distance"},
    template="plotly_white",
    color_discrete_sequence=["blue"]
)

# Layout for Dash
app.layout = html.Div([
    html.H1("Boston House Prices Dashboard", style={"textAlign": "center"}),
    
    html.Div([
        html.Div([
            html.H3("Summary Statistics", style={"textAlign": "center"}),
            html.P(f"Average Price: ${(1000 * data['PRICE'].mean()):.2f}"),
            html.P(f"Median Price: ${(1000 * data['PRICE'].median()):.2f}"),
            html.P(f"Number of Homes: {len(data)}")
        ], style={"width": "30%", "display": "inline-block", "verticalAlign": "top", "padding": "10px"}),

        html.Div([
            dcc.Graph(figure=house_price_fig)
        ], style={"width": "65%", "display": "inline-block", "padding": "10px"}),
    ]),

    html.Div([
        html.Div([
            dcc.Graph(figure=house_distance_fig)
        ], style={"width": "48%", "display": "inline-block", "padding": "10px"}),

        html.Div([
            dcc.Graph(figure=house_price_fig)
        ], style={"width": "48%", "display": "inline-block", "padding": "10px"}),
    ], style={"textAlign": "center"})
])

# Flask route
@server.route('/')
def index():
    return render_template('index.html')

@server.route('/info')
def info():
    return "<h1>Info Page</h1><p>This is a web app showcasing Boston house price data.</p>"

if __name__ == '__main__':
    server.run(debug=True)
