from django.shortcuts import render


def cart_summary(request):
    
    context = {

    }

    return render(request, 'store/cart/summary.html', context)
