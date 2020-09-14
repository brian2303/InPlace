"""InPlace URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path,include
from apps.landing_page.views import IndexView,IndexViewEnglish
from apps.login.views import DashboardView


urlpatterns = [
    path('admin/', admin.site.urls),
    # index dos idiomas
    path('', IndexView.as_view(),name='index'),
    path('en/', IndexViewEnglish.as_view(),name='index_english'),
    #url para graficos
    path('dashboard/',DashboardView.as_view(),name='dashboard'),
    # Modulos
    path('comercial/',include('apps.comercial.urls')),
    path('inventario/',include('apps.inventario.urls')),
    path('produccion/',include('apps.produccion.urls')),
    path('usuarios/',include('apps.usuarios.urls')),
    # Login
    path('login/',include('apps.login.urls'))
]
