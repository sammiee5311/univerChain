from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from univerchain.apps.orders.views import user_orders
from univerchain.apps.univercoin.ethereum import Ethereum

from .forms import EditForm, RegistrationForm
from .models import MyUser
from .tokens import account_activation_token

ethereum = Ethereum()


def register(request):
    if request.user.is_authenticated:
        return redirect("accounts:account")
    if request.method == "POST":
        regitseration_form = RegistrationForm(request.POST)

        if regitseration_form.is_valid():
            user = regitseration_form.save(commit=False)
            user.email = regitseration_form.cleaned_data["email"]
            user.set_password(regitseration_form.cleaned_data["password"])
            user.univercoin_account = regitseration_form.cleaned_data["univercoin_account"]
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            subject = "Ativate Account"
            message = render_to_string(
                "accounts/registration/email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": account_activation_token.make_token(user),
                },
            )
            user.email_user(subject=subject, message=message)
            return redirect("pages:home")
        else:
            return HttpResponse("Error", status=400)
    else:
        regitseration_form = RegistrationForm()

    return render(request, "accounts/registration/register.html", {"form": regitseration_form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = MyUser.objects.get(pk=uid)
    except BaseException:
        return render(request, "accounts/registration/invalid.html")
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        auth.login(request, user)
        return redirect("accounts:orders")
    else:
        return render(request, "accounts/registration/invalid.html")


@login_required
def account(request):
    return render(request, "accounts/user/account.html")


@login_required
def univercoin(request):
    account = request.user.ethereum_account
    contract = ethereum.Contract
    ether_state = True if contract else False
    coin = 0

    if ether_state:
        coin = contract.functions.balanceOf(account).call({"from": account})

    context = {"coin": coin}

    return render(request, "accounts/user/univercoin.html", context)


@login_required
def orders(request):
    orders = user_orders(request)
    context = {"orders": orders}

    return render(request, "accounts/user/orders.html", context)


@login_required
def edit_info(request):
    if request.method == "POST":
        edit_form = EditForm(instance=request.user, data=request.POST)

        if edit_form.is_valid():
            edit_form.save()

    else:
        edit_form = EditForm(instance=request.user)

    return render(request, "accounts/user/edit_info.html", {"edit_form": edit_form})


@login_required
def delete(request):
    user = MyUser.objects.get(username=request.user)
    user.is_active = False
    user.save()
    auth.logout(request)
    return redirect("accounts:delete_success")
