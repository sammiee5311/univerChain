from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from ether.ethereum import Ethereum

from .forms import RegisterationForm
from .models import myuser
from .tokens import account_activation_token

ethereum = Ethereum()


def register(request):
    if request.method == 'POST':
        registerForm = RegisterationForm(request.POST)

        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.email = RegisterationForm.cleaned_data['email']
            user.set_password(registerForm.cleaned_data['password'])
            user.ethereum_account(registerForm.cleaned_data['ethereum_account'])
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            subject = 'Ativate Account'
            message = render_to_string('accounts/registration/email.html', {
                'user': user,
                'domain': current_site.domain,
                'url': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user)})
            user.email_user(subject=subject, message=message)
    else:
        registerForm = RegisterationForm()

    return render(request, 'accounts/registeration/register.html', {'form': registerForm})


def activate(request):
    pass


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
