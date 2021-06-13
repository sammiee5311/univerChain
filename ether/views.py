from django.shortcuts import render
from .web import Web

w = Web()

web3 = w.connect_to_web3()
ABI = w.get_abi()
ADDRESS = '0x7E8351C38B1Df4366D3ED05A3a8C96340e80De25'
ether_state = False

try:
    account = web3.eth.accounts[0] # main account
    if ABI:
        contract = web3.eth.contract(address=ADDRESS, abi=ABI)

except AttributeError:
    print('web3 is not connected. Please, check your IP address or PORT')


def check(request):
    say = None

    try:
        say = contract.functions.say().call()
        ether_state = True
    except:
        """ error message """

    if request.method == 'POST':
        if ether_state:
            greeting = request.POST['greeting']
            contract.functions.setGreeting(greeting).transact({'from': account})
        else:
            """ error message """

    context = {
        'say' : say
    }

    return render(request, 'ether/main.html', context)

