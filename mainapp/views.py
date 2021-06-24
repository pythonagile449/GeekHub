from django.shortcuts import render
from mainapp.models import Hub, Article

# Create your views here.
from django.shortcuts import render

def mainpage(request):
    context = {
        'hubs': Hub.objects.all(),
        'articles': Article.objects.all()
    }

    return render(request, 'mainapp/index.html', context)

def hubs(request, hub_name):
    filtered_articles = Article.objects.filter(hub=hub_name)

    context = {
        'hub_name': hub_name,
        'hubs': Hub.objects.all(),
        'articles': filtered_articles
    }

    return render(request, 'mainapp/hub.html', context)
