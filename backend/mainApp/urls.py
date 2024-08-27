from django.urls import path

from mainApp import views



urls = [
    path('selectvalues/', views.SearchSelectValueView.as_view()),
    path('pacientes/', views.PacienteCreateView.as_view())
]