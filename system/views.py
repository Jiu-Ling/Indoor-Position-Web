import datetime
import copy

import numpy as np
from django.shortcuts import render
from django.contrib import messages
from django.core.files.uploadedfile import InMemoryUploadedFile
import pandas as pd
from pyecharts.charts.base import Base
# import custom utils
from util.Model_IDW import idw_model_for_rss
from util.Model_Loss import loss_model_for_rss
from util.Error_output import error_output
from util.convert import error_to_mem, result_to_mem, match_to_mem
from util.chartsTemplate import chartsError, charts3D, visualMap_3D
from util.io_util import create_excel
from .models import RSSRecord, RSSMatchData


def construct_chart(error_json, result_json, base_station_num, ap_data, point_data, step, x_min, y_min):
    template_error, template_3d = copy.deepcopy(chartsError), copy.deepcopy(charts3D)
    chart_error, chart_3D = Base(), Base()
    chart_error.options = template_error
    chart_3D.options = template_3d
    chart_error.options['xAxis']['data'] = error_json['xData']
    chart_error.options['yAxis']['data'] = error_json['yData']
    chart_error.options['series'][0]['data'] = error_json['rss1']
    # 待修改
    chart_error.options['series'][1]['data'] = []
    for i in range(len(point_data)):
        tmp_x = round((point_data[i][0] - x_min) * (1 / step), 2)
        tmp_y = round((point_data[i][1] - y_min) * (1 / step), 2)
        chart_error.options['series'][1]['data'].append([tmp_x , tmp_y])
    chart_3D.options['series'][0]['dimensions'] = ['x', 'y', 'z']
    for i in range(1, base_station_num + 1):
        chart_3D.options['series'][0]['dimensions'].append(f'RSS{i}')
    chart_3D.options['series'][0]['data'] = result_json
    chart_3D.options['series'][1]['data'] = [['x', 'y', 'z']]
    for i in range(len(ap_data)):
        chart_3D.options['series'][1]['data'].append([ap_data[i][0], ap_data[i][1], 3.24])
    chart_3D.options['series'][2]['data'] = [['x', 'y', 'z']]
    for i in range(len(point_data)):
        chart_3D.options['series'][2]['data'].append([point_data[i][0], point_data[i][1], 0])
    # 输出js格式str编码
    return chart_error.dump_options_with_quotes(), chart_3D.dump_options_with_quotes()


def upload(request):
    if request.method == 'POST':
        f = request.FILES.get('file')
        excel_type = f.name.split('.')[1]
        if excel_type in ['xlsx', 'xls']:
            try:
                data = pd.read_excel(f)
            except:
                error = '解析excel文件错误'
                messages.add_message(request, messages.ERROR, error)
                return render(request, "admin/statistics/upload.html")
            base_station_num = pd.to_numeric(request.POST.get('base_station_num'))
            step = pd.to_numeric(request.POST.get('step'))

            if base_station_num is not None or step is not None:
                error = '输入错误'
                if base_station_num <= 0 or step <= 0:
                    messages.add_message(request, messages.ERROR, error)
                    return render(request, "admin/statistics/upload.html")
            else:
                error = '输入错误'
                messages.add_message(request, messages.ERROR, error)
                return render(request, "admin/statistics/upload.html")

            res, df_idw, x_min, y_min = idw_model_for_rss(f, base_station_num, step)
            if res['status'] != 'success':
                messages.add_message(request, messages.ERROR, res['messages'])
                return render(request, "admin/statistics/upload.html")
            res, df_loss, ap_data, point_data = loss_model_for_rss(f, base_station_num, step)
            if res['status'] != 'success':
                messages.add_message(request, messages.ERROR, res['messages'])
                return render(request, "admin/statistics/upload.html")
            # 求差
            res, df_error = error_output(df_idw, df_loss, base_station_num)
            if res['status'] != 'success':
                messages.add_message(request, messages.ERROR, res['messages'])
                return render(request, "admin/statistics/upload.html")
            # 转换
            error_json = error_to_mem(df_error, base_station_num, x_min, y_min, step)
            result_json = result_to_mem(df_idw, base_station_num)
            # 构造图表
            chart_error, chart_3D = construct_chart(error_json, result_json,
                                                    base_station_num, ap_data, point_data, step, x_min, y_min)
            context = {
                'optionError': chart_error,
                'option3D': chart_3D,
            }
            io_idw = create_excel(df_idw)
            io_loss = create_excel(df_loss)
            # 将df_idw转换为一个文件并插入数据库
            RSSRecord.objects.create(
                user=request.user,
                name='idw_database' + datetime.datetime.now().strftime('%Y%m%d%H%M%S'),
                file=InMemoryUploadedFile(io_idw, None, 'idw_database_' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.xlsx', 'xlsx', io_idw.tell, None),
                model_name='IDW',
                base_station_num=base_station_num,
                step=step
            )
            # 将df_loss转换为一个文件并插入数据库
            RSSRecord.objects.create(
                user=request.user,
                name='loss_database' + datetime.datetime.now().strftime('%Y%m%d%H%M%S'),
                file=InMemoryUploadedFile(io_loss, None, 'loss_database_' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.xlsx', 'xlsx', io_loss.tell, None),
                model_name='LOSS',
                base_station_num=base_station_num,
                step=step
            )
            return render(request, 'admin/statistics/index.html', context)
        else:
            error = '上传文件类型错误！'
            messages.add_message(request, messages.ERROR, error)
            return render(request, 'admin/statistics/upload.html')
    else:
        return render(request, 'admin/statistics/upload.html')


def show_charts(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        # 检查id是否合法
        if not id.isdigit():
            messages.add_message(request, messages.ERROR, '输入ID错误')
            return show_select_list(request)
        record = RSSMatchData.objects.filter(id=id).first()
        if record is None:
            messages.add_message(request, messages.ERROR, '输入ID不存在')
            return show_select_list(request)
        # 展示图表，构建option
        df = pd.read_excel(record.file.file)
        chart_3D = Base()
        chart_Error = Base()
        chart_Error.options = copy.deepcopy(chartsError)
        chart_3D.options = copy.deepcopy(charts3D)
        chart_3D.options['series'][0]['dimensions'] = ['x', 'y', 'z', 'Euclidean_Location_Error']
        chart_3D.options['series'][0]['data'] = match_to_mem(df,
                                                             "Estimated_X_Euclidean",
                                                             "Estimated_Y_Euclidean",
                                                             "Euclidean_Location_Error")
        del chart_3D.options['series'][1], chart_3D.options['series'][1]
        chart_3D.options['visualMap'] = copy.deepcopy(visualMap_3D)
        chart_3D.options['visualMap'][0]['max'] = df['Euclidean_Location_Error'].max()
        chart_3D.options['visualMap'][0]['min'] = df['Euclidean_Location_Error'].min()
        # 设置标题
        chart_3D.options['visualMap'][0]['text'] = '误差'
        # chart_Error.options['title']['text'] = 'RSS误差图'
        # error_min, error_max = df['Euclidean_Location_Error'].min(), df['Euclidean_Location_Error'].max()
        # chart_Error.options['visualMap']['min'] = error_min
        # chart_Error.options['visualMap']['max'] = error_max
        # chart_Error.options['xAxis']['data'] = sorted(df['True_X'].tolist())
        # chart_Error.options['yAxis']['data'] = sorted(df['True_Y'].tolist())
        # chart_Error.options['series'][0]['data'] = []
        # chart_Error.options['series'][0]['name'] = 'Euclidean Location Error'
        # x_min, y_min = df['True_X'].min(), df['True_Y'].min()
        # x_length, y_length = df['True_X'].max() - x_min, df['True_Y'].max() - y_min
        # for i in range(len(df['Euclidean_Location_Error'])):
        #     chart_Error.options['series'][0]['data'].append([round((df['True_X'][i] - x_min) * np.sqrt(x_length), 3), round((df['True_Y'][i] - y_min) * np.sqrt(y_length), 3), df['Euclidean_Location_Error'][i]])
        # # 待修改
        del chart_Error.options['series'][1]
        # 输出js格式str编码
        option = chart_3D.dump_options_with_quotes()
        # optionError = chart_Error.dump_options_with_quotes()
        context = {
            'optionResult': option,
            # 'optionError': optionError
        }
        return render(request, 'admin/statistics/show_charts.html', context)
    else:
        return show_select_list(request)


def show_select_list(request):
    context = {
        'file_list': []
    }
    record = RSSMatchData.objects.filter(user=request.user).all()
    for i in record:
        context['file_list'].append({
            "name": i.name,
            "id": i.id
        })
    return render(request, 'admin/statistics/select_charts.html', context)
