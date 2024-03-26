from django.contrib import admin
from django.contrib import messages
from django.core.files.uploadedfile import InMemoryUploadedFile
from import_export.admin import ImportExportModelAdmin
from system.models import RSSMatchData
from util.FingerPointMatch import perform_localization
from util.io_util import create_excel
import datetime


@admin.register(RSSMatchData)
class RSSMatchDataAdmin(ImportExportModelAdmin):
    list_display = ("id", "user", "created_time", "db_file", "file", "test_file")
    list_filter = ("user", )
    empty_value_display = '空'
    list_per_page = 20

    action = ["show_charts"]
    # 添加或者修改数据时，不显示user字段
    exclude = ('user', 'created_time')

    # 添加数据时，可以上传test_file
    fields = ('db_file', 'test_file')
    # 修改数据时，可以上传test_file

    def show_charts(self, obj):
        return True
    show_charts.short_description = "显示图表"
    show_charts.type = 'primary'

    show_charts.action_url = '/view/show_charts/'
    show_charts.action_type = 1

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.name = 'RSSMatchData_' + datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        # 获取文件内容
        fingerprint_file = obj.db_file.file
        test_file = obj.test_file.file
        base_station_num = obj.db_file.base_station_num
        res, df = perform_localization(fingerprint_file, test_file, base_station_num)
        if res['status'] != 'success':
            messages.add_message(request, messages.ERROR, res['messages'])
            return False
        io_excel = create_excel(df)
        obj.file = InMemoryUploadedFile(io_excel, None, 'RSSMatchData_' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.xlsx', 'xlsx', io_excel.tell, None)
        messages.add_message(request, messages.SUCCESS, 'RSS匹配成功')
        super().save_model(request, obj, form, change)
