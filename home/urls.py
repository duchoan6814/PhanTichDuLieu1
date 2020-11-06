from django.urls import path
from . import views

urlpatterns = [
  path('', views.index),
  path('data-analysis', views.dataAnalysis),
  path('simple-chart', views.simpleChart)
]