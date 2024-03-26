from django.db import models
from django.contrib.auth.models import User


class RSSRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    name = models.CharField(max_length=50, verbose_name="名称")
    file = models.FileField(upload_to='upload/model_result/', verbose_name="文件")
    model_name = models.CharField(max_length=50, verbose_name="模型", default='')
    base_station_num = models.IntegerField(verbose_name="基站数量")
    step = models.IntegerField(verbose_name="步长")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_time']
        verbose_name = 'RSS拟合历史记录'
        verbose_name_plural = 'RSS拟合历史记录'


# 创建匹配后数据表
class RSSMatchData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    name = models.CharField(max_length=50, verbose_name="名称")
    db_file = models.ForeignKey(RSSRecord, on_delete=models.CASCADE, verbose_name="RSS指纹数据库")
    file = models.FileField(upload_to='upload/match_result/', verbose_name="结果文件")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    test_file = models.FileField(upload_to='upload/test_file/', verbose_name="测试文件")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_time']
        verbose_name = 'RSS指纹匹配'
        verbose_name_plural = 'RSS指纹匹配'
