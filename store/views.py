from django.shortcuts import render

from .models import Category, Product


def categories(request):
    return {
        'categories': Category.objects.all()
    }

def products(request):
    prods = Product.objects.all()

    context = {
        'products' : prods
    }
    return render(request, 'store/main.html', context)
