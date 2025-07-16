from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages


def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, 'Parollar mos emas')
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Bu nom bilan oldin ro‘yxatdan o‘tilgan')
            return redirect('signup')

        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password1
        )
        messages.success(request, 'Tabriklaymiz! Ro‘yxatdan o‘tdingiz.')
        return redirect('login')

    return render(request, 'account/signup.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if not username or not password:
            messages.error(request, 'Maʼlumotlarni to‘liq kiriting')
            return redirect('login')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Siz login qildingniz!')
            return redirect('index')
        else:
            messages.error(request, 'Login yoki parol noto‘g‘ri')
            return redirect('login')

    return render(request, 'account/login.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'Siz dasturdan chiqdingiz')
    return redirect('index')
