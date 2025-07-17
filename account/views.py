from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import SignUpForm, LoginForm

# def signup_view(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         first_name = request.POST['first_name']
#         last_name = request.POST['last_name']
#         email = request.POST['email']
#         password1 = request.POST['password1']
#         password2 = request.POST['password2']
#
#         if password1 != password2:
#             messages.error(request, 'Parollar mos emas')
#             return redirect('signup')
#
#         if User.objects.filter(username=username).exists():
#             messages.error(request, 'Bu nom bilan oldin ro‘yxatdan o‘tilgan')
#             return redirect('signup')
#
#         user = User.objects.create_user(
#             username=username,
#             first_name=first_name,
#             last_name=last_name,
#             email=email,
#             password=password1
#         )
#         messages.success(request, 'Tabriklaymiz! Ro‘yxatdan o‘tdingiz.')
#         return redirect('login')
#
#     return render(request, 'account/signup.html')
#
#
# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#
#         if not username or not password:
#             messages.error(request, 'Maʼlumotlarni to‘liq kiriting')
#             return redirect('login')
#
#         user = authenticate(username=username, password=password)
#
#         if user is not None:
#             login(request, user)
#             messages.success(request, 'Siz login qildingniz!')
#             return redirect('index')
#         else:
#             messages.error(request, 'Login yoki parol noto‘g‘ri')
#             return redirect('login')
#
#     return render(request, 'account/login.html')
#
#
def logout_view(request):
    logout(request)
    messages.success(request, 'Siz dasturdan chiqdingiz')
    return redirect('index')


from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Siz dasturga kirdingiz.')
            return redirect('index')
        else:
            print(form.errors)
            messages.error(request, 'Login yoki parol noto‘g‘ri.')
    else:
        form = LoginForm(request)
    return render(request, 'account/login.html', {'form': form})

def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Bu username orqali oldin ro‘yxatdan o‘tilgan.')
                return redirect('signup')
            user = form.save()
            login(request, user)
            messages.success(request, 'Muvaffaqiyatli ro‘yxatdan o‘tdingiz!')
            return redirect('login')
        else:
            messages.error(request, 'Formada xatolik bor.')
    else:
        form = SignUpForm()
    return render(request, 'account/signup.html', {'form': form})



































