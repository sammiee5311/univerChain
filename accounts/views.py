from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from ether.ethereum import Ethereum

from .forms import EditForm, RegisterationForm
from .models import myuser
from .tokens import account_activation_token

ethereum = Ethereum()


def register(request):
    if request.method == 'POST':
        regitseration_form = RegisterationForm(request.POST)

        if regitseration_form.is_valid():
            user = regitseration_form.save(commit=False)
            user.email = regitseration_form.cleaned_data['email']
            user.set_password(regitseration_form.cleaned_data['password'])
            user.ethereum_account = regitseration_form.cleaned_data['ethereum_account']
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            subject = 'Ativate Account'
            message = render_to_string('accounts/registeration/email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user)})
            user.email_user(subject=subject, message=message)
            return redirect('index')
    else:
        regitseration_form = RegisterationForm()

    return render(request, 'accounts/registeration/register.html', {'form': regitseration_form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = myuser.objects.get(pk=uid)
    except():
        pass
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        auth.login(request, user)
        return redirect('accounts:dashboard')
    else:
        return render(request, 'accounts/registeration/invalid.html')


@login_required
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

    return render(request, 'accounts/user/dashboard.html', context)


@login_required
def edit_info(request):
    if request.method == 'POST':
        edit_form = EditForm(instance=request.user, data=request.POST)

        if edit_form.is_valid():
            edit_form.save()

    else:
        edit_form = EditForm(instance=request.user)

    return render(request, 'accounts/user/edit_info.html', {'edit_form': edit_form})


@login_required
def delete(request):
    user = myuser.objects.get(username=request.user)
    user.is_active = False
    user.save()
    auth.logout(request)
    return redirect('accounts:delete_success')
