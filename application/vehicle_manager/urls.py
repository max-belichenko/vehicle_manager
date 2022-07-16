from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from api.views.datalog import DataLogView
from api.views.user import UserViewSet, GroupViewSet
from api.views.vehicle import VehicleList, VehicleDetail


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('vehicles/', VehicleList.as_view()),
    path('vehicles/<int:pk>/', VehicleDetail.as_view()),
    path('log/', DataLogView.as_view()),
]
