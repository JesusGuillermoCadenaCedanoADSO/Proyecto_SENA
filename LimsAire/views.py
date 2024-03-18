from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from .models import UnidadDeMedicion, Parametros, FactorDeConversion, CadenaDeCustodia, Mediciones
from .forms import UnidadForm, ParametroForm, FactorForm, CadenaForm, MedicionForm
from django.views import generic


from .models import Parametros, UnidadDeMedicion, FactorDeConversion, CadenaDeCustodia, Mediciones

# Create your views here.

def home(request):
    """View function for home page of site."""
    return render(request, 'home.html')


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


@login_required
def crear_parametro(request):
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
            return redirect('home')
        except ValueError:
            return render(request, 'crear_parametro.html', {'form': ParametroForm, 'error': 'Ingresar datos válidos'})


@login_required
def listar_parametros(request):
    lista_parametros = Parametros.objects.filter(user=request.user)
    return render(request, 'listar_parametros.html', {'lista_parametros': lista_parametros})

@login_required
def parametro_detail(request, parametro_id):
    if request.method == 'GET':
        parametro = get_object_or_404(Parametros, pk=parametro_id, user=request.user)
        form = ParametroForm(instance=parametro)
        return render(request, 'parametro_detail.html', {'parametro': parametro,'form':form})
    else:
        try:
            parametro = get_object_or_404(Parametros, pk=parametro_id, user=request.user)
            form = ParametroForm(request.POST, instance=parametro)
            form.save()
            return redirect('listar_parametros')
        except ValueError:
            return render(request, 'parametro_detail.html', {'parametro': parametro, 'form': form, 'error': "Error actualizando parametro"})


@login_required
def eliminar_parametro(request, parametro_id):
    parametro = get_object_or_404(Parametros, pk=parametro_id, user=request.user)
    if request.method == 'POST':
        parametro.delete()
        return redirect('listar_parametros')


@login_required
def crear_unidad(request):
    
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
            return redirect('home')
        except ValueError:
            return render(request, 'crear_unidad.html', {'form': UnidadForm, 'error': 'Ingresar datos válidos'})


@login_required
def listar_unidades(request):
    lista_unidades = UnidadDeMedicion.objects.filter(user=request.user)
    return render(request, 'listar_unidades.html', {'lista_unidades': lista_unidades})


@login_required
def unidad_detail(request, unidad_id):
    if request.method == 'GET':
        unidad = get_object_or_404(UnidadDeMedicion, pk=unidad_id, user=request.user)
        form = UnidadForm(instance=unidad)
        return render(request, 'unidad_detail.html', {'unidad': unidad,'form':form})
    else:
        try:
            unidad = get_object_or_404(UnidadDeMedicion, pk=unidad_id, user=request.user)
            form = UnidadForm(request.POST, instance=unidad)
            form.save()
            return redirect('listar_unidades')
        except ValueError:
            return render(request, 'unidad_detail.html', {'unidad': unidad, 'form': form, 'error': "Error actualizando unidad"})
        
@login_required
def eliminar_unidad(request, unidad_id):
    unidad = get_object_or_404(UnidadDeMedicion, pk=unidad_id, user=request.user)
    if request.method == 'POST':
        unidad.delete()
        return redirect('listar_unidades')


@login_required
def crear_factor(request):
    
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
            return redirect('home')
        except ValueError:
            return render(request, 'crear_factor.html', {'form': FactorForm, 'error': 'Ingresar datos válidos'})

@login_required
def listar_factores(request):
    lista_factores = FactorDeConversion.objects.filter(user=request.user)
    return render(request, 'listar_factores.html', {'lista_factores': lista_factores})

@login_required
def factor_detail(request, factor_id):
    if request.method == 'GET':
        factor = get_object_or_404(FactorDeConversion, pk=factor_id, user=request.user)
        form = FactorForm(instance=factor)
        return render(request, 'factor_detail.html', {'factor': factor,'form':form})
    else:
        try:
            factor = get_object_or_404(FactorDeConversion, pk=factor_id, user=request.user)
            form = FactorForm(request.POST, instance=factor)
            form.save()
            return redirect('listar_factores')
        except ValueError:
            return render(request, 'factor_detail.html', {'factor': factor, 'form': form, 'error': "Error actualizando factor"})

@login_required
def eliminar_factor(request, factor_id):
    factor = get_object_or_404(FactorDeConversion, pk=factor_id, user=request.user)
    if request.method == 'POST':
        factor.delete()
        return redirect('listar_factores')

@login_required
def crear_cadena(request):
    
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
            return redirect('home')
        except ValueError:
            return render(request, 'crear_cadena.html', {'form': CadenaForm, 'error': 'Ingresar datos válidos'})

@login_required
def listar_cadenas(request):
    lista_cadenas = CadenaDeCustodia.objects.filter(user=request.user)
    return render(request, 'listar_cadenas.html', {'lista_cadenas': lista_cadenas})

@login_required
def cadena_detail(request, cadena_id):
    if request.method == 'GET':
        cadena = get_object_or_404(CadenaDeCustodia, pk=cadena_id, user=request.user)
        form = CadenaForm(instance=cadena)
        return render(request, 'cadena_detail.html', {'cadena': cadena,'form':form})
    else:
        try:
            cadena = get_object_or_404(CadenaDeCustodia, pk=cadena_id, user=request.user)
            form = CadenaForm(request.POST, instance=cadena)
            form.save()
            return redirect('listar_cadenas')
        except ValueError:
            return render(request, 'cadena_detail.html', {'cadena': cadena, 'form': form, 'error': "Error actualizando cadena"})

@login_required
def eliminar_cadena(request, cadena_id):
    cadena = get_object_or_404(CadenaDeCustodia, pk=cadena_id, user=request.user)
    if request.method == 'POST':
        cadena.delete()
        return redirect('listar_cadenas')


@login_required
def crear_medicion(request):
    
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
            return redirect('home')
        except ValueError:
            return render(request, 'crear_medicion.html', {'form': MedicionForm, 'error': 'Ingresar datos válidos'})


@login_required
def listar_mediciones(request):
    lista_mediciones = Mediciones.objects.filter(user=request.user)
    return render(request, 'listar_mediciones.html', {'lista_mediciones': lista_mediciones})


@login_required
def medicion_detail(request, medicion_id):
    if request.method == 'GET':
        medicion = get_object_or_404(Mediciones, pk=medicion_id, user=request.user)
        form = MedicionForm(instance=medicion)
        return render(request, 'medicion_detail.html', {'medicion': medicion,'form':form})
    else:
        try:
            medicion = get_object_or_404(Mediciones, pk=medicion_id, user=request.user)
            form = MedicionForm(request.POST, instance=medicion)
            form.save()
            return redirect('listar_mediciones')
        except ValueError:
            return render(request, 'medicion_detail.html', {'medicion': medicion, 'form': form, 'error': "Error actualizando medicion"})

@login_required
def eliminar_medicion(request, medicion_id):
    medicion = get_object_or_404(Mediciones, pk=medicion_id, user=request.user)
    if request.method == 'POST':
        medicion.delete()
        return redirect('listar_mediciones')