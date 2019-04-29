import pygrib
import os
import numpy as np


def grb_to_grid(grb_obj):
    """Takes a single grb object containing multiple
    levels. Assumes same time, pressure levels. Compiles to a cube"""
    n_levels = len(grb_obj)
    levels = np.array([grb_element['level'] for grb_element in grb_obj])
    indexes = np.argsort(levels)[::-1] # highest pressure first
    cube = np.zeros([n_levels, grb_obj[0].values.shape[0], grb_obj[1].values.shape[1]])
    for i in range(n_levels):
        cube[i,:,:] = grb_obj[indexes[i]].values
    cube_dict = {'data' : cube, 'units' : grb_obj[0]['units'],
                 'levels' : levels[indexes]}
    return cube_dict

def get_data_as_cube_and_lats_lons(file_path, file_name, data_type):
    grbs = pygrib.open(os.path.join(file_path, file_name))
    grbs.messages
    grb = grbs.readline()
    lats,lons = grb.latlons()
    grb_data = grbs.select(name=data_type)
    grb_cube_data=grb_to_grid(grb_data)

    forecast_date = grb.validDate
    issuance_date = grb.analDate
    grbs.close()

    return grb_cube_data, lats, lons, forecast_date, issuance_date

