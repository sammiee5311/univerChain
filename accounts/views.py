from django.contrib import auth, messages
from django.shortcuts import redirect, render
from ether.ethereum import Ethereum

from .models import myuser

ethereum = Ethereum()


def register(request):
    if request.method == 'POST':
        request_info = request.POST
        first_name = request_info['first_name']
        last_name = request_info['last_name']
        username = request_info['username']
        email = request_info['email']
        password = request_info['password']
        password_confirm = request_info['password_confirm']
        ethereum_account = request_info['etherAccount']
        if password == password_confirm:
            if myuser.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
                return redirect('register')
            else:
                if myuser.objects.filter(email=email).exists():
                    messages.error(request, 'Email already exists')
                    return redirect('register')
                else:
                    user = myuser.objects.create_user(username=username, password=password, email=email,
                                                      first_name=first_name, last_name=last_name,
                                                      ethereum_account=ethereum_account)
                    user.save()
                    # auth.login(request, user)
                    messages.success(request, 'Register Successfully')
                    return redirect('login')
        else:
            messages.error(request, 'Passwords do not macth')
            return redirect('register')

    return render(request, 'accounts/register.html')


def login(request):
    if request.method == 'POST':
        request_info = request.POST
        username, password = request_info['username'], request_info['password']

        user = auth.authenticate(username=username, password=password)

        if user:
            auth.login(request, user)
            messages.success(request, 'Login Succeeded')
            return redirect('index')
        else:
            messages.error(request, 'Login Failed')
            return redirect('index')

    return render(request, 'accounts/login.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'Logged Out Succeeded')

    return redirect('index')


def dashboard(request):
    account = request.user.ethereum_account
    contract = ethereum.Contract
    ether_state = True if contract else False
    coin = 0

    if ether_state:
        coin = contract.functions.balanceOf(account).call({'from': account})
    context = {
        'coin': coin,
    }

    return render(request, 'accounts/dashboard.html', context)
