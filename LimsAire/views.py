from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.messages import get_messages 
from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from .models import UnidadDeMedicion, Parametros, FactorDeConversion, CadenaDeCustodia, Mediciones
from .forms import UnidadForm, ParametroForm, FactorForm, CadenaForm, MedicionForm
from django.views import generic

from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework import viewsets
from .serializers import UnidadDeMedicionSerializer, ParametroSerializer, FactorSerializer, CadenaSerializer, MedicionSerializer
from django.http import JsonResponse
from rest_framework.views import APIView
import json

# Tu código de vista aquí



from .models import Parametros, UnidadDeMedicion, FactorDeConversion, CadenaDeCustodia, Mediciones

# Create your views here.

def home(request):
    """View function for home page of site."""
    return render(request, 'home.html')

def mi_vista(request,ruta):
    if request.method == 'POST':
        storage=get_messages(request)
        for message in storage:
            pass
        return redirect(ruta)
    

def signup(request):
    if request.method == 'GET':
        render(request, 'signup.html', {'form': UserCreationForm})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'signup.html', {'form': UserCreationForm, 'error': 'Este usuario ya está registrado'})
        return render(request, 'signup.html', {'form': UserCreationForm, 'error': 'Las constraseñas no coinciden'})
    return render(request, 'signup.html', {'form': UserCreationForm})


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {'form': AuthenticationForm})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {'form': AuthenticationForm,
                                                   'error': 'Username or password is incorrect'})
        else:
            login(request, user)
            return redirect('home')

@login_required
def signout(request):
    logout(request)
    return redirect('home')

@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def crear_parametro(request):
    if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
        if request.method == 'GET':
            return render(request, 'crear_parametro.html', {
                'form': ParametroForm
            })
        else:
            try:
                
                form = ParametroForm(request.POST)
                nuevo_parametro = form.save(commit=False)
                nuevo_parametro.user = request.user
                nuevo_parametro.save()
                messages.success(request, '¡El parámetro se ha creado exitosamente!')
                return redirect('crear_parametro')
            except ValueError:
                messages.error(request, 'Ingresar datos válidos')
                return render(request, 'crear_parametro.html', {'form': ParametroForm})
    else:
        if request.method=='GET':
            data = {
                "user":"id (entero) de usuario",
                "nombre":"Nombre de parámetro",
                "simbolo":"Simbolo de parámetro",
                "pmolecular":"Peso molecular en g/mol"
            }
            return Response(data)
        elif request.method =='POST':
            serializer = ParametroSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def listar_parametros(request):
    if request.method == 'GET':
        lista_parametros = Parametros.objects.filter(user=request.user)
        serializer =  ParametroSerializer(lista_parametros,context={'request':request},many=True)
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'listar_parametros.html', {'lista_parametros': lista_parametros})
        else:
            return Response(serializer.data)

@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def parametro_detail(request, parametro_id):
    if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
        if request.method == 'GET':
            parametro = get_object_or_404(Parametros, pk=parametro_id, user=request.user)
            form = ParametroForm(instance=parametro)
            return render(request, 'parametro_detail.html', {'parametro': parametro,'form':form})
        else:
            try:
                
                parametro = get_object_or_404(Parametros, pk=parametro_id, user=request.user)
                form = ParametroForm(request.POST, instance=parametro)
                form.save()
                messages.success(request, '¡El parámetro ' + str(parametro_id) + ' se ha actualizado exitosamente!')
                return redirect('listar_parametros')
            except ValueError:
                messages.error(request, 'Ingresar datos válidos')
                return render(request, 'parametro_detail.html', {'parametro': parametro, 'form': form})
    else:
        if request.method == 'GET':
            lista_parametros = Parametros.objects.filter(user=request.user, pk=parametro_id)
            serializer = ParametroSerializer(lista_parametros, many=True)
            return Response(serializer.data)
        else:
            parametro=get_object_or_404(Parametros, pk=parametro_id)
            serializer = ParametroSerializer(parametro, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=400)


@api_view(['POST', 'DELETE'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def eliminar_parametro(request, parametro_id):
    parametro = get_object_or_404(Parametros, pk=parametro_id, user=request.user)
    if request.method == 'POST':
        parametro.delete()
        return redirect('listar_parametros')
    elif request.method == 'DELETE':
    # Eliminar la unidad y devolver una respuesta de éxito
        parametro.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def crear_unidad(request):
    if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
        if request.method == 'GET':
            return render(request, 'crear_unidad.html', {
                'form': UnidadForm
            })
        else:
            try:
                form = UnidadForm(request.POST)
                nuevo_unidad = form.save(commit=False)
                nuevo_unidad.user = request.user
                nuevo_unidad.save()
                messages.success(request, '¡La unidad se ha creado exitosamente!')
                return redirect('crear_unidad')
            except ValueError:
                messages.error(request, 'Ingresar datos válidos')
                return render(request, 'crear_unidad.html', {'form': UnidadForm})
    else:
        if request.method == 'GET':
            data = {
            "user":"id (entero) de usuario",
            "nombre": "Nombre de la unidad",
            "simbolo": "Simbolo de la unidad"
            }
            return Response(data)
        elif request.method == 'POST':
            serializer = UnidadDeMedicionSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def listar_unidades(request):
    if request.method == 'GET':
        lista_unidades = UnidadDeMedicion.objects.filter(user=request.user)
        #lista_unidades = UnidadDeMedicion.objects.all()
        serializer = UnidadDeMedicionSerializer(lista_unidades, context={'request': request},many=True)
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'listar_unidades.html', {'lista_unidades': lista_unidades})
        else:
            return Response(serializer.data)



@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def unidad_detail(request, unidad_id):
    if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
        if request.method == 'GET':
            unidad = get_object_or_404(UnidadDeMedicion, pk=unidad_id, user=request.user)
            form = UnidadForm(instance=unidad)
            return render(request, 'unidad_detail.html', {'unidad': unidad,'form':form})
        else:
            try:
                unidad = get_object_or_404(UnidadDeMedicion, pk=unidad_id, user=request.user)
                form = UnidadForm(request.POST, instance=unidad)
                form.save()
                messages.success(request, '¡La unidad ' + str(unidad_id) + ' se ha actualizado exitosamente!')
                #render(request, 'unidad_detail.html', {'unidad': unidad, 'form': form})
                return redirect('listar_unidades')
            except ValueError:
                messages.error(request, 'Ingresar datos válidos')
                return render(request, 'unidad_detail.html', {'unidad': unidad, 'form': form})
    else:
        if request.method == 'GET':
            lista_unidades = UnidadDeMedicion.objects.filter(user=request.user, pk=unidad_id)
            serializer = UnidadDeMedicionSerializer(lista_unidades, many=True)
            return Response(serializer.data)
        else:
            unidad=get_object_or_404(UnidadDeMedicion, pk=unidad_id)
            serializer = UnidadDeMedicionSerializer(unidad, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=400)

@api_view(['POST', 'DELETE'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def eliminar_unidad(request, unidad_id):
    # Obtener la unidad a eliminar
    unidad = get_object_or_404(UnidadDeMedicion, pk=unidad_id, user=request.user)

    if request.method == 'POST':
        # Eliminar la unidad y redireccionar a la lista de unidades
        unidad.delete()
        return redirect('listar_unidades')
    
    elif request.method == 'DELETE':
        # Eliminar la unidad y devolver una respuesta de éxito
        unidad.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)





@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def crear_factor(request):
    if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
        if request.method == 'GET':
            return render(request, 'crear_factor.html', {
                'form': FactorForm
            })
        else:
            try:
                
                form = FactorForm(request.POST)
                nuevo_factor = form.save(commit=False)
                nuevo_factor.user = request.user
                nuevo_factor.save()
                messages.success(request, '¡El factor se ha creado exitosamente!')
                return redirect('crear_factor')
            except ValueError:
                messages.error(request, 'Ingresar datos válidos')
                return render(request, 'crear_factor.html', {'form': FactorForm})
    else:
        if request.method == 'GET':
            data = {
            "user":"Número que representa id del usuario",
            "parametro": "Número que representa id del parámetro",
            "unidad_origen": "Número que representa id de unidad que se desea cambiar",
            "unidad_destino": "Número que representa id de unidad que se desea obtener",
            "factor":"Número que representa factor de conversión"
            }
            return Response(data)
        elif request.method == 'POST':
            serializer = FactorSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def listar_factores(request):
    if request.method == 'GET':
        lista_factores = FactorDeConversion.objects.filter(user=request.user)
        serializer = FactorSerializer(lista_factores, context={'request': request},many=True)
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'listar_factores.html', {'lista_factores': lista_factores})
        else:
            return Response(serializer.data)

@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def factor_detail(request, factor_id):
    if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
        if request.method == 'GET':
            factor = get_object_or_404(FactorDeConversion, pk=factor_id, user=request.user)
            form = FactorForm(instance=factor)
            return render(request, 'factor_detail.html', {'factor': factor,'form':form})
        else:
            try:
                
                factor = get_object_or_404(FactorDeConversion, pk=factor_id, user=request.user)
                form = FactorForm(request.POST, instance=factor)
                form.save()
                messages.success(request, '¡El factor ' + str(factor_id) + ' se ha actualizado exitosamente!')
                return redirect('listar_factores')
            except ValueError:
                messages.error(request, 'Ingresar datos válidos')
                return render(request, 'factor_detail.html', {'factor': factor, 'form': form})
    else:
        if request.method == 'GET':
            lista_factores = FactorDeConversion.objects.filter(user=request.user, pk=factor_id)
            serializer = FactorSerializer(lista_factores, many=True)
            return Response(serializer.data)
        else:
            factor=get_object_or_404(FactorDeConversion, pk=factor_id)
            serializer = FactorSerializer(factor, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=400)


@api_view(['POST', 'DELETE'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def eliminar_factor(request, factor_id):
    factor = get_object_or_404(FactorDeConversion, pk=factor_id, user=request.user)
    if request.method == 'POST':
        factor.delete()
        return redirect('listar_factores')
    elif request.method == 'DELETE':
        # Eliminar la unidad y devolver una respuesta de éxito
        factor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def crear_cadena(request):
    if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
        if request.method == 'GET':
            return render(request, 'crear_cadena.html', {
                'form': CadenaForm
            })
        else:
            try:
                
                form = CadenaForm(request.POST)
                nuevo_cadena = form.save(commit=False)
                nuevo_cadena.user = request.user
                nuevo_cadena.save()
                messages.success(request, '¡La cadena se ha creado exitosamente!')
                return redirect('crear_cadena')
            except ValueError:
                messages.error(request, 'Ingresar datos válidos')
                return render(request, 'crear_cadena.html', {'form': CadenaForm})
    else:
        if request.method == 'GET':
            data ={
                    "user": "Número que representa id del usuario",
                    "idcadena": "Número que representa id de cadena nueva",
                    "parametro": 'Lista que incluye id de parametro. ejemplo:["1"]',
                    "cliente": "Nombre de cliente",
                    "proyecto": "Nombre de proyecto",
                    "ciudad": "Nombre de ciudad",
                    "muestreado_por": "Nombre de persona que hizo el muestreo",
                    "punto_de_muestreo": "Nombre de punto donde se hizo el muestreo",
                    "coordenada_norte": "Coordenada norte de punto donde se hizo el muestreo",
                    "coordenada_este": "Coordenada este de punto donde se hizo el muestreo",
                    "altura": "Altura de punto donde se hizo el muestreo en msnm",
                    "observaciones": "Observaciones durante el muestreo"
                }
            return Response(data)
        elif request.method == 'POST':
            serializer = CadenaSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def listar_cadenas(request):
    if request.method == 'GET':
        lista_cadenas = CadenaDeCustodia.objects.filter(user=request.user)
        serializer = CadenaSerializer(lista_cadenas, context={'request': request},many=True)
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'listar_cadenas.html', {'lista_cadenas': lista_cadenas})
        else:
            return Response(serializer.data)

@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def cadena_detail(request, cadena_id):
    if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
        if request.method == 'GET':
            cadena = get_object_or_404(CadenaDeCustodia, pk=cadena_id, user=request.user)
            form = CadenaForm(instance=cadena)
            return render(request, 'cadena_detail.html', {'cadena': cadena,'form':form})
        else:
            try:
                
                cadena = get_object_or_404(CadenaDeCustodia, pk=cadena_id, user=request.user)
                form = CadenaForm(request.POST, instance=cadena)
                form.save()
                messages.success(request, '¡La cadena ' + str(cadena_id) + ' se ha actualizado exitosamente!')
                return redirect('listar_cadenas')
            except ValueError:
                messages.error(request, 'Ingresar datos válidos')
                return render(request, 'cadena_detail.html', {'cadena': cadena, 'form': form})
    else:
        if request.method == 'GET':
            lista_cadenas = CadenaDeCustodia.objects.filter(user=request.user, pk=cadena_id)
            serializer = CadenaSerializer(lista_cadenas, many=True)
            return Response(serializer.data)
        else:
            cadena=get_object_or_404(CadenaDeCustodia, pk=cadena_id)
            serializer = CadenaSerializer(cadena, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=400)

@api_view(['POST', 'DELETE'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def eliminar_cadena(request, cadena_id):
    cadena = get_object_or_404(CadenaDeCustodia, pk=cadena_id, user=request.user)
    if request.method == 'POST':
        cadena.delete()
        return redirect('listar_cadenas')
    elif request.method == 'DELETE':
        # Eliminar la unidad y devolver una respuesta de éxito
        cadena.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def crear_medicion(request):
    if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
        if request.method == 'GET':
            return render(request, 'crear_medicion.html', {
                'form': MedicionForm
            })
        else:
            try:
                form = MedicionForm(request.POST)
                nuevo_medicion = form.save(commit=False)
                nuevo_medicion.user = request.user
                nuevo_medicion.save()
                messages.success(request, '¡La medicion se ha creado exitosamente!')
                return redirect('crear_medicion')
            except ValueError:
                messages.error(request, 'Ingresar datos válidos')
                return render(request, 'crear_medicion.html', {'form': MedicionForm})
    else:
        if request.method == 'GET':
            data = {
            "user": "Número que representa id del usuario",
            "fechamedicion": "Fecha en la que se realizó la medición",
            "hora": "Hora en la que se realizó la medición",
            "resultado":"Número que representa el resultado de la medición",
            "cadena_custodia": "Número que representa id de la cadena de custodia",
            "parametro": "Número que representa id del parámetro asociado a la medición",
            "unidad_de_medida": "Número que representa id de la unidad de medida",
            "unidad_de_conversion": "Número que representa id de la unidad de conversión",
            }
            return Response(data)
        elif request.method == 'POST':
            serializer = MedicionSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def listar_mediciones(request):
    if request.method == 'GET':
        lista_mediciones = Mediciones.objects.filter(user=request.user)
        serializer = MedicionSerializer(lista_mediciones, context={'request': request},many=True)
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'listar_mediciones.html', {'lista_mediciones': lista_mediciones})
        else:
            return Response(serializer.data)


@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def medicion_detail(request, medicion_id):
    if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
        if request.method == 'GET':
            medicion = get_object_or_404(Mediciones, pk=medicion_id, user=request.user)
            form = MedicionForm(instance=medicion)
            return render(request, 'medicion_detail.html', {'medicion': medicion,'form':form})
        else:
            try:
                
                medicion = get_object_or_404(Mediciones, pk=medicion_id, user=request.user)
                form = MedicionForm(request.POST, instance=medicion)
                form.save()
                mi_vista(request,'listar_mediciones')
                messages.success(request, '¡La medición' + str(medicion_id) + ' se ha actualizado exitosamente!')
                return redirect('listar_mediciones')
            except ValueError:
                messages.error(request, 'Ingresar datos válidos')
                return render(request, 'medicion_detail.html', {'medicion': medicion, 'form': form})
    else:
        if request.method == 'GET':
            lista_mediciones = Mediciones.objects.filter(user=request.user, pk=medicion_id)
            serializer = MedicionSerializer(lista_mediciones, many=True)
            return Response(serializer.data)
        else:
            medicion=get_object_or_404(Mediciones, pk=medicion_id)
            serializer = MedicionSerializer(medicion, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=400)

@api_view(['POST', 'DELETE'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def eliminar_medicion(request, medicion_id):
    medicion = get_object_or_404(Mediciones, pk=medicion_id, user=request.user)
    if request.method == 'POST':
        medicion.delete()
        return redirect('listar_mediciones')
    elif request.method == 'DELETE':
        # Eliminar la unidad y devolver una respuesta de éxito
        medicion.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# funcion experimental para probar api no logro autenticar correctamente al usuario

@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def FVistaUnidadApi(request):
    #if request.user.is_authenticated:
    if request.method == 'GET':
        unidades = UnidadDeMedicion.objects.all()
        serializer = UnidadDeMedicionSerializer(unidades, many=True)
        # Verifica si el cliente acepta JSON como respuesta
        if 'application/json' in request.META.get('HTTP_ACCEPT', ''):
            # Si la solicitud acepta JSON, devuelve JSON
            return Response(serializer.data)
        else:
            return render(request, 'listar_unidades.html', {'lista_unidades': serializer.data})

#----------------------------------------------------------------------------------
 
class VistaUnidadApi(viewsets.ModelViewSet):
    serializer_class = UnidadDeMedicionSerializer
    queryset = UnidadDeMedicion.objects.all()

class ExampleView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        content = {
            'user': str(request.user),  # `django.contrib.auth.User` instance.
            'auth': str(request.auth),  # None
        }
        return Response(content)