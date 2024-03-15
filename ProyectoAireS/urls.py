"""
URL configuration for ProyectoAireS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from LimsAire import views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('crear_parametro/', views.crear_parametro, name='crear_parametro'),
    path('listar_parametros/', views.listar_parametros, name='listar_parametros'),
    path('listar_parametros/<int:parametro_id>/', views.parametro_detail, name='parametro_detail'),
    path('listar_parametros/<int:parametro_id>/delete', views.eliminar_parametro, name='eliminar_parametro'),
    path('crear_unidad/', views.crear_unidad, name='crear_unidad'),
    path('listar_unidades/', views.listar_unidades, name='listar_unidades'),
    path('listar_unidades/<int:unidad_id>/', views.unidad_detail, name='unidad_detail'),
    path('listar_unidades/<int:unidad_id>/delete', views.eliminar_unidad, name='eliminar_unidad'),
    path('crear_factor/', views.crear_factor, name='crear_factor'),
    path('logout/', views.signout, name='logout'),
    path('signin/', views.signin, name='signin'),

    
]

