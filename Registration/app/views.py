from django.shortcuts import render, redirect , get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .forms import UserRegisterForm
from django.contrib.auth.forms import UserCreationForm

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = UserCreationForm()
    return render(request, 'registration.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, 'Invalid username or password')
    form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def home(request):
    users = User.objects.all()
    if request.method == 'POST':
        if 'update' in request.POST:
            user_id = request.POST.get('user_id')
            new_username = request.POST.get('new_username')
            user = get_object_or_404(User, pk=user_id)
            user.username = new_username
            user.save()
            messages.success(request, f'Username updated successfully!')
            return redirect('home')
        elif 'delete' in request.POST:
            user_id = request.POST.get('user_id')
            user = get_object_or_404(User, pk=user_id)
            user.delete()
            messages.success(request, f'User deleted successfully!')
            return redirect('home')
    return render(request, 'homepage.html', {'users': users})