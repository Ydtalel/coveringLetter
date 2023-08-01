from django.contrib import admin
from django.urls import path, include
from userProfile import urls as userProfile_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(userProfile_urls)),
]
