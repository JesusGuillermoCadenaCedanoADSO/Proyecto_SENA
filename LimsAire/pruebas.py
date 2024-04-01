from django.contrib.auth.models import User
from models import UnidadDeMedicion


usuario = User.objects.create_user(username='jesuscadena', password='123')
unidad=UnidadDeMedicion.objects.create(
        user=usuario,nombre='partes por mil', simbolo='ppt'
    )
print(unidad)