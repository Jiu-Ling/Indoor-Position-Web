from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from system.models import RSSRecord


@admin.register(RSSRecord)
class RSSRecordAdmin(ImportExportModelAdmin):
    list_display = ("id", "user", "model_name", "base_station_num", "step", "created_time", "file")
    list_filter = ("user", "base_station_num")
    empty_value_display = '空'
    list_per_page = 20
    
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False