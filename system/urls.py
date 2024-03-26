from django.urls import path
from django.urls import include
from .views import show_charts, upload

urlpatterns = [
    path('view/upload/', upload, name='upload'),
    path('view/show_charts/', show_charts, name='show_charts'),
]
