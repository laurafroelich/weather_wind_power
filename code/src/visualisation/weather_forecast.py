import plotly.graph_objs as go
import numpy as np
import ipywidgets

from weather_wind.visualisation.geography import get_rotated_basemap, get_coastline_traces, get_country_traces
from weather_wind.data_retrieval.weather_forecast import get_data_as_cube_and_lats_lons


def rotate_data_and_lats(grb_matrix_data, lons, degrees=180):
    lons_rotated = lons.copy()
    lons_rotated[lons >= degrees] = lons[lons >= degrees] - (2*degrees)

    # proper rotation obtained from: https://plot.ly/ipython-notebooks/basemap-maps/
    i_east = lons_rotated[0, :] >= 0  # indices of east lon
    i_west = lons_rotated[0, :] < 0   # indices of west lon

    # stack the two halves
    lons_rotated = np.hstack((lons_rotated[:, i_west], lons_rotated[:, i_east]))

    # Correspondingly, shift the data array
    data_rotated = np.hstack((grb_matrix_data[:, i_west], grb_matrix_data[:, i_east]))

    return data_rotated, lons_rotated


def get_widget_figure(file_path, file_name, data_type, degrees_to_rotate=180):
    grb_cube_data, lats, lons, forecast_date, issuance_date = get_data_as_cube_and_lats_lons(
        file_path, file_name, data_type)
    matrix_data = grb_cube_data['data'][10]
    data_rotated, lons_rotated = rotate_data_and_lats(matrix_data, lons)
    basemap_rotated = get_rotated_basemap()

    anno_text = str(forecast_date) + '<br>(issued on ' + str(issuance_date) + ')'
    # "Data courtesy of
    # <a href='http://www.esrl.noaa.gov/psd/data/composites/day/'>\
    # NOAA Earth System Research Laboratory</a>"

    axis_style = dict(
        zeroline=False,
        showline=False,
        showgrid=False,
        ticks='',
        showticklabels=False,
    )

    layout1 = go.Layout(
        title=go.layout.Title(
            text=data_type,
            xref='paper',
            x=0
        ),
        showlegend=False,
        hovermode="closest",  # highlight closest point on hover
        margin={'t': 100, 'b': 60, 'l': 60, 'r': 0, 'pad': 8},
        xaxis=go.layout.XAxis(
            axis_style,
            range=[-degrees_to_rotate, degrees_to_rotate]  # restrict y-axis to range of lon
        ),
        yaxis=go.layout.YAxis(
            axis_style,
            range=[-85, 85]
        ),
        annotations=[
            dict(
                text=anno_text,
                xref='paper',
                yref='paper',
                x=0,
                y=1,
                yanchor='bottom',
                showarrow=False,
                align='left'
            )
        ],
        autosize=False,
        width=500,
        height=400
    )

    traces_cc = get_coastline_traces(basemap_rotated)+get_country_traces(basemap_rotated)

    fw = go.FigureWidget(data=traces_cc + [go.Contour(z=data_rotated, x=lons_rotated[0, :],
                                                      y=lats[:, 0])], layout=layout1)
    return fw


def get_figure_with_subplots(file_path, file_name, data_types, degrees_to_rotate=180):

    fw1 = get_widget_figure(file_path, file_name, data_types[0], degrees_to_rotate=degrees_to_rotate)
    fw2 = get_widget_figure(file_path, file_name, data_types[1], degrees_to_rotate=degrees_to_rotate)

    fig_subplots = ipywidgets.VBox([fw1, fw2], layout=ipywidgets.Layout(display='flex',
                                                                        flex_flow='column',
                                                                        align_items='center',
                                                                        width='100%'))
    return fig_subplots
