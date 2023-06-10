#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import requests
import json

class InfuraConnector():

    def __init__(self,
                 api_key,
                 base_url ='https://mainnet.infura.io/v3',
                 ):

        if base_url.endswith('/'):
            base_url = base_url[:-1]
        self.base_url = '%s/%s'%(base_url,api_key)

        self.session = requests.Session()
        self.session.headers.update({'User-agent':'InfuraConnector','Content-Type': 'application/json'})

    def request(self,parameters):
        parameters.update({"jsonrpc":"2.0","id":1})

        r = self.session.post(url=self.base_url,json=parameters).json()

        if 'error' in r:
            raise Exception(r['error'])

        return r

    def eth_gasPrice(self):
        parameters = {'method': 'eth_gasPrice', "params": []}
        r = self.request(parameters)
        return int(r['result'], 16)

    def eth_getBlockByNumber(self,block_parameter,show_transaction_details=False):
        """
            BLOCK PARAMETER [required] - hexadecimal block number, or the string "latest", "earliest" or "pending".
            SHOW TRANSACTION DETAILS FLAG [required] - if set to true, it returns the full transaction objects, if false only the hashes of the transactions.
        """
        if isinstance(block_parameter,int):
            block_parameter = "0x%x"%(block_parameter)

        parameters = {"method": "eth_getBlockByNumber", "params":[block_parameter,show_transaction_details]}
        r = self.request(parameters)['result']
        for k in {'difficulty','gasLimit','gasUsed','number','size','timestamp','totalDifficulty'}:
            if r[k][0:2]=="0x":
                r[k] = int(r[k],base=16)
        return r

    def eth_getTransactionReceipt(self,transaction_hash):
        "TRANSACTION HASH [required] - a string representing the hash (32 bytes) of a transaction"
        parameters = {"method": "eth_getTransactionReceipt", "params":[transaction_hash]}
        r = self.request(parameters)['result']

        for k in {'blockNumber','cumulativeGasUsed','effectiveGasPrice','gasUsed','status','transactionIndex','type'}:
            if r[k][0:2]=="0x":
                r[k] = int(r[k],base=16)

        return r

def get_block_detail():
    b = ic.eth_getBlockByNumber(17265811,True)
    for t in b['transactions']:
        t['receipt'] = ic.eth_getTransactionReceipt(t['hash'])

    return b


if __name__=="__main__":
    ic = InfuraConnector('16aef963ac304b66b9d697fb65d79806')
    #print(ic.eth_gasPrice())
    #print(ic.eth_getBlockByNumber(10000))
    #print(ic.eth_getBlockByNumber('latest'))
    print(ic.eth_getTransactionReceipt('0xc5549fbad9833ab9ed38e7f3a1d5512c74b35a9d87a76fe0f15c6128ddd8b546'))
    #print(get_block_detail())
