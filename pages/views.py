from django.shortcuts import render


def index(request):

    if request.method == 'POST':
        category = request.POST['category']
        print(category)
    context = {
        'title': 'index'
    }

    return render(request, 'pages/index.html', context)
