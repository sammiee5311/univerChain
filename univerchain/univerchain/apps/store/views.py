from django.shortcuts import get_object_or_404, render

from .models import Category, Product


def category_list(request, category_slug=None):
    category_name = category_slug.replace("-", " ")
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(
        category__in=Category.objects.get(name=category_name).get_descendants(include_self=True), is_active=True
    )

    context = {"category": category, "products": products}

    return render(request, "store/category.html", context)


def product_all(request):
    products = Product.objects.prefetch_related("product_image").filter(is_active=True)

    context = {"products": products}

    return render(request, "store/main.html", context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)

    context = {"product": product}

    return render(request, "store/detail.html", context)
