from web3 import Web3
from typing import Any, Dict
import sys
import getopt
import yaml

class Ethereum:
    def __init__(self) -> None:
        self.ip = 'localhost' # default ip
        self.port = '8545' # default port
        self.filename = './files/abi.yml' # default abi file
        self.SMART_CONTRACT_ADDRESS = '0x575fc0F0916aCd9E3CB6Ed0DAd5E952cc0636075'
        self.SMART_CONTTRACT_ABI = self.get_abi()
        self.web3 = self.connect_to_web3()
        self.__contract = self.get_contract()

    def connect_to_web3(self) -> Any:
        w3 = Web3(Web3.HTTPProvider(f'http://{self.ip}:{self.port}'))

        if w3.isConnected():
            return w3
        else:
            return None

    def get_abi(self) -> Dict:
        abi = None
        try:
            with open(self.filename) as f:
                abi = yaml.load(f, Loader=yaml.FullLoader)
        except FileNotFoundError:
            print('Please, check your file name.')

        return abi

    def get_contract(self):
        try:
            return self.web3.eth.contract(address=self.SMART_CONTRACT_ADDRESS, abi=self.SMART_CONTTRACT_ABI)
        except AttributeError:
            print('web3 is not connected. Please, check your IP address or PORT')
            return None

    @property
    def Contract(self):
        return self.__contract


if __name__ == '__main__':
    conn = Connect()
    conn.connect_to_web3()
