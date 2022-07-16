from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from api.views.user import UserViewSet, GroupViewSet


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/', include('api.urls')),
]
