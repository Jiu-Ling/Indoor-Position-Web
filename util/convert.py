# Description: 数据转换工具
def error_to_mem(df, base_station_num, x_min, y_min, step=1):
    res = {
        'xData': df['x'].tolist(), 'yData': df['y'].tolist()
    }
    for j in range(1, base_station_num + 1):
        res[f'rss{j}'] = []
        for i in range(len(df['x'].tolist())):
            res[f'rss{j}'].append([round((res['xData'][i] - x_min) * round(1 / step, 2), 3), round((res['yData'][i] - y_min) * round(1 / step, 2), 3), abs(df[f'RSS{j}'][i])])
    # x列去重
    res['xData'] = sorted(list(set(df['x'].tolist())))
    res['yData'] = sorted(list(set(df['y'].tolist())))

    res['xData'] = [round(i, 3) for i in res['xData']]
    res['yData'] = [round(i, 3) for i in res['yData']]

    return res


def result_to_mem(df, base_station_num):
    columns = ['x', 'y', 'z']
    for i in range(0, base_station_num):
        columns.append('RSS' + str(i + 1))
    res = [
        columns
    ]
    for i in range(len(df['x'].tolist())):
        tmp = [round(df['x'][i], 3), round(df['y'][i], 3), 0]
        for j in range(1, base_station_num + 1):
            tmp.append(df[f'RSS{j}'][i])
        res.append(tmp)

    return res


def match_to_mem(df, x_col_name, y_col_name, error_col_name):
    columns = ['x', 'y', 'z', 'Euclidean_Location_Error']
    res = [
        columns
    ]
    for i in range(len(df[x_col_name].tolist())):
        tmp = [round(df[x_col_name][i], 3), round(df[y_col_name][i], 3), 0, round(df[error_col_name][i], 3)]
        res.append(tmp)

    return res
