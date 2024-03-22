from django.urls import path, include
from rest_framework import routers
from LimsAire import views

router=routers.DefaultRouter()
router.register(r'unidades',views.VistaUnidadApi,'unidades')

urlpatterns=[
    path('api/v1/', include(router.urls))
]

