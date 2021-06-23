from django.shortcuts import get_object_or_404, render

from .models import Category, Product


def categories(request):
    return {
        'categories': Category.objects.all()
    }


def category_list(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)

    context = {
        'category': category,
        'products': products
    }

    return render(request, 'store/category.html', context)


def products(request):
    prods = Product.objects.all()

    context = {
        'products': prods
    }

    return render(request, 'store/main.html', context)


def product_detail(request, slug):
    prod = get_object_or_404(Product, slug=slug, in_stock=True)

    context = {
        'product': prod
    }

    return render(request, 'store/detail.html', context)
