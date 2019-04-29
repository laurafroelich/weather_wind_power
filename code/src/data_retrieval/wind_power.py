import pandas as pd


def get_produced_wind_power(file_path):
    df = pd.read_html(file_path)[0]
    data_df = df['Wind power DK in MWh']['Data was last updated 01-01-2019'].copy()
    data_df = data_df.rename(columns={'Unnamed: 0_level_2': 'Date'})
    data_df['start_hour'] = data_df['Hours'].apply(lambda x: x.split('-')[0].split('\xa0')[0])

    data_df['date_time'] = data_df['Date'] + ' ' + data_df['start_hour']
    data_df['date_time'] = pd.to_datetime(data_df['date_time'])
    data_df = data_df.sort_values('date_time')

    return data_df
