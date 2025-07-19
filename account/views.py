from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import SignUpForm, LoginForm, ChangePassForm,ResetPassForm
from .utils import generate_code, send_to_mail

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

def change_pass_view(request):
    if request.method == 'GET':
        code = generate_code()
        request.session['verification_code'] = code
        send_to_mail(request.user.email, code)
        messages.info(request, 'kod yuborildi')
        form = ChangePassForm()
        return render(request, 'account/change_pass.html', {'form':form})

    else:
        form = ChangePassForm(request.POST)
        if form.is_valid():
            old_pass = form.cleaned_data['old_pass']
            new_pass = form.cleaned_data['new_pass']
            code = form.cleaned_data['code']
            session_code = request.session.get('verification_code')

            if not request.user.check_password(old_pass):
                messages.error(request, 'eski parolni xato kiritdingiz')
                return redirect('change-pass')
            if session_code!=code:
                messages.error(request, 'kod xato')
                return redirect('change-pass')
            user = request.user
            user.set_password(new_pass)
            user.save()
            messages.success(request, 'parolingiz ozgartirildi')
            update_session_auth_hash(request, user)
            del request.session['verification_code']
            return redirect('profile')
        return redirect('change-pass')

from datetime import datetime,timedelta

def reset_pass(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            user = User.objects.get(username=username)
            code = generate_code()
            request.session['reset_code'] = code
            request.session['username'] = username
            request.session['created_at'] = datetime.now().isoformat()


            send_to_mail(user.email, code)
            return redirect('reset2')
        except User.DoesNotExist:
            return render(request, 'account/reset-pass1.html')
    return render(request, 'account/reset-pass1.html')

def reset_pass2(request):
    if request.method == 'POST':
        form = ResetPassForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            code = form.cleaned_data['code']
            session_code = request.session.get('reset_code')
            username = request.session.get('username')
            created_at = request.session.get('created_at')

            if session_code!=code:
                messages.error(request, 'kod xato')
                return redirect('change-pass')

            if created_at:
                created_at = datetime.fromisoformat(created_at)
                if datetime.now() - created_at > timedelta(minutes=1):
                    messages.info(request, 'Tasdiqlash kodi eskirgan.')
                    return redirect('reset2')

            try:
                user = User.objects.get(username=username)
                user.set_password(password)
                user.save()
                messages.success(request, 'Parolingiz muvaffaqiyatli o‘zgartirildi.')
                del request.session['reset_code']
                del request.session['username']
                return redirect('login')
            except User.DoesNotExist:
                messages.error(request, 'Foydalanuvchi topilmadi.')
                return redirect('reset')
    else:
        form = ResetPassForm()

    return render(request, 'account/reset-pass2.html', {'form': form})























