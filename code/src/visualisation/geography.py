import os

#from mpl_toolkits.basemap import Basemap
import cartopy
import numpy as np

import plotly.graph_objs as go
import plotly.figure_factory as ff
import cartopy.crs as ccrs
import matplotlib.pyplot as plt


# Make trace-generating function (return a Scatter object)
def make_scatter(x,y):
    return go.Scatter(
        x=x,
        y=y,
        mode='lines',
        line=go.scatter.Line(color="black"),
        name=' '  # no name on hover
    )


# Functions converting coastline/country polygons to lon/lat traces
def polygons_to_traces(poly_paths, N_poly, basemap_map):
    '''
    pos arg 1. (poly_paths): paths to polygons
    pos arg 2. (N_poly): number of polygon to convert
    '''
    traces = []  # init. plotting list

    for i_poly in range(N_poly):
        poly_path = poly_paths[i_poly]

        # get the Basemap coordinates of each segment
        coords_cc = np.array(
            [(vertex[0],vertex[1])
             for (vertex,code) in poly_path.iter_segments(simplify=False)]
        )

        # convert coordinates to lon/lat by 'inverting' the Basemap projection
        lon_cc, lat_cc = basemap_map(coords_cc[:,0],coords_cc[:,1], inverse=True)

        # add plot.ly plotting options
        traces.append(make_scatter(lon_cc,lat_cc))

    return traces


# Function generating coastline lon/lat traces
def get_coastline_traces(basemap_map):
    #poly_paths = basemap_map.drawcoastlines().get_paths() # coastline polygon paths
    #N_poly = 91 # use only the 91st biggest coastlines (i.e. no rivers)
    return cartopy.mpl.patch.geos_to_path(basemap_map.coastlines()) # polygons_to_traces(poly_paths, N_poly, basemap_map)


# Function generating country lon/lat traces
def get_country_traces(basemap_map):
    #poly_paths = basemap_map.drawcountries().get_paths() # country polygon paths
    #N_poly = len(poly_paths)  # use all countries
    return basemap_map.coastlines() #polygons_to_traces(poly_paths, N_poly, basemap_map)


def get_rotated_basemap(degrees=180):
    #m_rotated = Basemap(llcrnrlon = 1 - degrees, llcrnrlat = -89, urcrnrlon = degrees,
    #                    urcrnrlat = 89 , projection = 'mill', area_thresh =10000,
    #                    resolution='l')
    #m_rotated = cartopy.crs.Miller(central_longitude=0.0, globe=None)



    m_rotated = plt.axes(projection=ccrs.PlateCarree())
    #ax.coastlines()

    return m_rotated
