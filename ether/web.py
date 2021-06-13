from web3 import Web3
from typing import Any, Dict
import sys
import getopt
import yaml

class Web:
    def __init__(self) -> None:
        self.ip = 'localhost' # default ip
        self.port = '8545' # default port
        self.filename = './files/abi.yml' # default abi file

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


if __name__ == '__main__':
    conn = Connect()
    conn.connect_to_web3()
