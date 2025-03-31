'''
Assignment 7
CP321

Author: Mustafa Ali (169076982)
Date: 1 April 2025
'''

import numpy as np
import pandas as pd
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import plotly.graph_objects as go

from datetime import datetime
import yfinance as yf


def fifa_data():
    data = pd.read_csv("Data/FIFA.csv")
    
    i, c = np.unique(data["Winners"], return_counts = True)
    out = pd.Series(c, index = i)
    country = out.index.tolist()
    wins = out.tolist()
    for i, v in enumerate(country):
        country[i] = v[:-1] # Weird symbol at the end of each country name
    data1 = {'Country': country, 'Wins': wins} 
    df = pd.DataFrame(data1)
    return data, df


app = Dash()
server = app.server

app.layout = [
    html.H1("FIFA World Cup Data", style={"color":"black", "font-family":"Verdana", "textAlign":"center", "padding":"auto"}),
    html.Br(),
    html.Div([dcc.Graph(id="world-cup")]),
    dcc.Dropdown(['Argentina', 'Brazil', 'UK', 'France', 'Germany', 'Italy', 'Spain', 'Uruguay'], 'Brazil', id='country-dropdown'),
    html.Div([html.P(id='number-of-wins',children="Select a Country")]),
    html.Br(),
    dcc.Dropdown([1930, 1934, 1938, 1950, 1954, 1958, 1962, 1966, 1970, 1974, 1978, 1982, 1986, 1990, 1994, 1998, 2002, 2006, 2010, 2014, 2018, 2022], 2022, id='year-dropdown'),
    html.Div([html.P(id='year-winners',children="Select a Year")]),
    html.Br()
]


@callback(
    [Output('world-cup', 'figure'),
     Output('number-of-wins', 'children'),
    Output('year-winners', 'children')],
    [Input('country-dropdown', 'value'),
     Input('year-dropdown', 'value')]
    
)
def update_graph(country, year):
    df1 = fifa_data()[0]
    df2 = fifa_data()[1]
    fig = go.Figure(data=go.Choropleth(
        locationmode="country names",
        locations = df2["Country"],
        z = df2['Wins'],
        text = df2['Country'],
        colorscale = 'Greens',
        autocolorscale=False,
        reversescale=False,
        marker_line_color='green',
        marker_line_width=0.5,
        colorbar_title = 'Number of Wins',))
    
    fig.update_layout(
        title_text='Choropleth of FIFA World Cup Winners',
        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='equirectangular'
        )
    )
    
    if country:
        country_wins = df2[df2["Country"] == country].iloc[0,1]
        if country_wins == 1:
            country_win_str = f"{country} won the FIFA World cup once!"
        else:
            country_win_str = f"{country} won the FIFA World cup {country_wins} times!"
    else:
        country_win_str = "Select a country"

    if year:
        year_winner = df1[df1["Year"] == year].iloc[0,1]
        year_winner_str = f"{year_winner}won the FIFA World cup in {year}"
    else:
        country_win_str = "Select a year"
    
    return fig, country_win_str, year_winner_str
    

if __name__ == "__main__":
    app.run(debug=True)
