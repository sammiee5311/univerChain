from django.contrib import messages
from django.shortcuts import render

from .ethereum import Ethereum

ethereum = Ethereum()


def check_univercoin(request):
    registered = 'You have not checked it yet.'

    if request.method == 'POST':
        account = request.POST['etherAccount']
        contract = ethereum.Contract
        ether_state = True if contract else False

        if ether_state and 'type_name' in request.POST:
            type_name = request.POST['type_name']
            grade = request.POST['grade']
            try:
                contract.functions.register(type_name, int(grade)).transact({'from': account})
            except:
                messages.error(request, 'User already existed.')

        elif ether_state and 'registered' in request.POST:
            registered = contract.functions.checkRegistered().call({'from': account})
            registered = 'currently registered' if registered else 'you are not registered.'
        else:
            """ error message """

    context = {
        'registered': registered
    }

    return render(request, 'ether/check_univercoin.html', context)
