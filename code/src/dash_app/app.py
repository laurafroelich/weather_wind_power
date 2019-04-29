import dash
import dash_core_components as dcc
import dash_html_components as html
import os
import plotly.graph_objs as go
import pandas as pd



import weather_wind.data_retrieval.wind_power
import weather_wind.visualisation.wind_power
import weather_wind.visualisation.weather_forecast
from weather_wind.visualisation.weather_forecast import get_country_traces, get_coastline_traces, \
    get_rotated_basemap, get_data_as_cube_and_lats_lons, rotate_data_and_lats

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

data_folder = os.path.join(os.path.expanduser('~'), 'Documents', 'Projects', 'WeatherWind', 'data')
data_file = 'wind-power-dk_2018_hourly.xls'
file_path = os.path.join(data_folder, data_file)

df = weather_wind.data_retrieval.wind_power.get_produced_wind_power(file_path)

fig_data = weather_wind.visualisation.wind_power.get_wind_power_production_scatter_data(df)

#weather_forecast = weather_wind.visualisation.weather_forecast.get_figure_with_subplots(
#    data_folder, 'gfs_3_20180508_0600_027.grb2', ["V component of wind", "U component of wind"])
#basemap_rotated = get_rotated_basemap()
#map_traces = get_coastline_traces(basemap_rotated) #+get_country_traces(basemap_rotated)
grb_cube_data, lats, lons, forecast_date, issuance_date = get_data_as_cube_and_lats_lons(
    data_folder, 'gfs_3_20180508_0600_027.grb2', "V component of wind")
matrix_data = grb_cube_data['data'][10]
wind_v, lons_rotated = rotate_data_and_lats(matrix_data, lons)

# code to draw map taken from tutorial at https://plot.ly/python/choropleth-maps/
# WIP: get contours drawn on top of map instead of example agricultural data
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2011_us_ag_exports.csv')

for col in df.columns:
    df[col] = df[col].astype(str)

scl = [
    [0.0, 'rgb(242,240,247)'],
    [0.2, 'rgb(218,218,235)'],
    [0.4, 'rgb(188,189,220)'],
    [0.6, 'rgb(158,154,200)'],
    [0.8, 'rgb(117,107,177)'],
    [1.0, 'rgb(84,39,143)']
]

df['text'] = df['state'] + '<br>' + \
             'Beef ' + df['beef'] + ' Dairy ' + df['dairy'] + '<br>' + \
             'Fruits ' + df['total fruits'] + ' Veggies ' + df['total veggies'] + '<br>' + \
             'Wheat ' + df['wheat'] + ' Corn ' + df['corn']

data = [go.Choropleth(
    colorscale = scl,
    autocolorscale = False,
    locations = df['code'],
    z = df['total exports'].astype(float),
    locationmode = 'USA-states',
    text = df['text'],
    marker = go.choropleth.Marker(
        line = go.choropleth.marker.Line(
            color = 'rgb(255,255,255)',
            width = 2
        ))
)]

layout = go.Layout(
    title = go.layout.Title(
        text = 'Wind speed forecast (V component)'
    ),
    geo = go.layout.Geo(
        scope = 'world',
        projection = go.layout.geo.Projection(type = 'miller'),
        showlakes = True,
        lakecolor = 'rgb(255, 255, 255)',
        showcoastlines=True,
        showland=True,
        showcountries=True,
        lonaxis = {'range': (-90, 90)},
        lataxis = {'range': (0, 360)}
    ),
)

app.layout = html.Div(
    children=[
        html.H1(children='Wind speed and wind power produced',
                style={'textAlign': 'center', 'color': colors['text']},),
        html.Div(children='''Visualise to look for relations between wind speed and wind power produced.''',
                 style={'textAlign': 'center', 'color': colors['text']}),
        dcc.Graph(
            id='produced-wind-power',
            figure={
                'data': fig_data,
                'layout': {
                    'title': 'Wind power produced (MWh)',
                    'plot_bgcolor': colors['background'],
                    'paper_bgcolor': colors['background'],
                    'font': {'color': colors['text']}
                }
            }
        ),
        dcc.Graph(
            figure=go.Figure(data = data,
                             layout = layout)),
        dcc.Graph(
            figure=go.Figure(data = [go.Contour(z=matrix_data,
                                         x=lons_rotated[0, :],
                                         y=lats[:, 0],
                                         opacity=0.8,
                                         contours={'coloring': 'fill'}),
                                     ],
                             layout = layout))
    ],
    style={'backgroundColor': colors['background']})

if __name__ == '__main__':
    app.run_server(debug=True)
