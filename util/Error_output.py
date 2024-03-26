import pandas as pd
import numpy as np


def error_output(df_idw, df_loss, base_station_num):
    columns = ['x', 'y']
    for i in range(0, base_station_num):
        columns.append('RSS' + str(i + 1))
    df_error = pd.DataFrame(columns=columns)

    df_error['x'] = df_idw['x']
    df_error['y'] = df_idw['y']
    # 对两个表的RSS1列求差
    for i in range(1, base_station_num + 1):
        df_error[f'RSS{i}'] = df_idw[f'RSS{i}'] - df_loss[f'RSS{i}']

    return {'status': 'success'}, df_error
