"""gringo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path
from stock import views
from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required


urlpatterns = [
	path('stock/', views.stock),
	path('campaña/', views.campaña),

    path('campaña/nueva', login_required(views.CampañaCreate.as_view())),
	path('mov_gral/', views.mov_gral),
    path('admin/', admin.site.urls),

    # Other URL patterns ...
    url(r'^accounts/', include('django_registration.backends.activation.urls')),
    url(r'^accounts/', include('django.contrib.auth.urls')),
]
