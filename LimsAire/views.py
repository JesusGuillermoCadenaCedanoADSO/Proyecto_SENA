from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from .models import UnidadDeMedicion, Parametros
from .forms import UnidadForm, ParametroForm, FactorForm
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
        print(unidad_id)
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