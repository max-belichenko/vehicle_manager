from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from api import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('vehicles/', views.VehicleList.as_view()),
    path('vehicles/<int:pk>/', views.VehicleDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
