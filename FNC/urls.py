from . import views
from django.urls import path

urlpatterns = [
    path('', views.FNC, name="FNC"),
    path('show_graph/<str:logic_phrase_type>/<str:logic_phrase>/', views.show_graph, name='show_graph'),
]
