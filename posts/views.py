from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import *
from django.contrib import messages
def index(request):
    categories = Category.objects.all()
    first_news = []
    for category in categories:
        category_first_post = News.objects.filter(category=category).order_by('-id').first()
        if category_first_post is not None:
            first_news.append(category_first_post)
    if len(first_news)<4:
        news = News.objects.all().order_by("-id")
        first_news.extend(news[len(news)-4: len(news)-len(first_news)])
    news = News.objects.all().order_by('-id')
    return render(request, 'index.html', {
        'categories': categories,
        'first_news': first_news,
        'news': news
    })

def category(request, pk):
    category = Category.objects.get(id=pk)
    news = News.objects.filter(category=category).order_by('-id')
    return render(request, 'category-01.html', {'news': news})

def news_detail(request, pk):
    post = News.objects.get(pk=pk)

    if request.method == "POST":
        comment = request.POST.get('msg')
        if request.user.is_authenticated:
            Comment.objects.create(
                news=post,
                pos_text=comment,
                user=request.user
            )
            messages.info(request, 'Fikr-mulohaza uchun rahmat!')
        else:
            messages.error(request, 'Fikr qoldirish uchun iltimos tizimga kiring.')
            return redirect('login')

    comments = Comment.objects.filter(news=post).order_by('-id')

    return render(request, 'blog-detail-01.html', {
        'post': post,
        'comments': comments
    })

@login_required(login_url='login')
def profile(request):
    user = User.objects.get(username=request.user.username)
    return render(request, 'account/profile.html', {'user': user})
