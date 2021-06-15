from django.shortcuts import render
from .ethereum import Ethereum

ethereum = Ethereum()

def check(request):
    say = None
   
    if request.method == 'POST':
        account = request.POST['etherAccount']
        contract = ethereum.Contract
        ether_state = True if contract else False
            
        if ether_state and 'greeting' in request.POST:
            greeting = request.POST['greeting']
            contract.functions.setGreeting(greeting).transact({'from': account})
        elif ether_state and 'say' in request.POST:
            say = contract.functions.say().call()
        else:
            """ error message """

    context = {
        'say' : say
    }

    return render(request, 'ether/main.html', context)

