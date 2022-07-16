from django.urls import path

from api.views.datalog import DataLogView
from api.views.vehicle import VehicleList, VehicleDetail


urlpatterns = [
    path('vehicles/', VehicleList.as_view()),
    path('vehicles/<int:pk>/', VehicleDetail.as_view()),
    path('logs/', DataLogView.as_view()),
]
