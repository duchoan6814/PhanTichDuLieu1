from django.urls import path
from . import views

urlpatterns = [
  path('', views.index),
  path('data-analysis', views.dataAnalysis),
  path('simple-chart', views.simpleChart),
  path('simple-chart/newCase', views.simpleChart),
  path('simple-chart/newDeath', views.newDeath),
  path('simple-chart/tileCaseWithDeath', views.tileCaseWithDeath),
  path('simple-chart/macVaChetTheoThang', views.macVaChetTheoThang)
]