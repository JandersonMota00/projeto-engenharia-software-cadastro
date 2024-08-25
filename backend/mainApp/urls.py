from django.urls import path

from mainApp import views



urls = [
    path('/dynamicselect/<str:optionname>/<str:searchterm>', views.getOptions),
    path('seed', views.seed),
    path('', views.home)
]