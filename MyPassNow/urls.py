from django.urls import include, path
from django.contrib import admin
from rest_framework import routers
from .API import views

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path(r'api/', views.apiRoot),
    path(r'api/users/', views.UserList.as_view()),
    path(r'api/user/<str:username>/', views.UserObj.as_view()),
    path(r'api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path(r'admin/', admin.site.urls),
]