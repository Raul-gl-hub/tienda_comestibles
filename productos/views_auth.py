# productos/views_auth.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages

def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            messages.success(request, "Registro exitoso.")
            return redirect('inicio')
        else:
            messages.error(request, "Error en el registro. Verifica los datos.")
    else:
        form = UserCreationForm()
    return render(request, 'productos/registro.html', {'form': form})

def iniciar_sesion(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            usuario = form.get_user()
            login(request, usuario)
            messages.success(request, f"Bienvenido {usuario.username}!")
            return redirect('inicio')
        else:
            messages.error(request, "Error en el inicio de sesión.")
    else:
        form = AuthenticationForm()
    return render(request, 'productos/iniciar_sesion.html', {'form': form})

def cerrar_sesion(request):
    logout(request)
    messages.info(request, "Has cerrado sesión.")
    return redirect('inicio')