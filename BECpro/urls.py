"""BECpro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
<<<<<<< HEAD
    path('accounts/', include('accounts.urls')),
    path('', include('members.urls')),
    path('staff', include('staff.urls')),
=======

    path('', include('members.urls')),
    path('staff/', include('staff.urls')),
>>>>>>> 3d40901ea8dc265b5366c0af6bbc19d7433d0ce2
    path('authenticate/', include('authenticate.urls')),
    
]
