import plotly.graph_objs as go


def get_wind_power_production_scatter_data(data_df):
    trace1 = go.Scatter(x=data_df['date_time'],
                        y=data_df['DK1'],
                        mode='lines+markers',
                        name='DK1')
    trace2 = go.Scatter(x=data_df['date_time'],
                        y=data_df['DK2'],
                        mode='lines+markers',
                        name='DK2')
    data = [trace1, trace2]

    return data
