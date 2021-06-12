from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    context = {
        'title' : 'index'
    }

    return render(request, 'pages/index.html', context)