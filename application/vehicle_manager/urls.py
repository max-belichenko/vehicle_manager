from django.urls import path, include
from rest_framework import routers

from api.views.user import UserViewSet, GroupViewSet


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('api/', include('api.urls')),
]
