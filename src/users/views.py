from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from finance.models import Account, Category, Transaction


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
        return render(request, 'users/register.html', {'form': form})
    else:
        form = RegisterForm()
        return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    user = request.user
    accounts = Account.objects.filter(user=user)
    return render(request, 'users/profile.html')

