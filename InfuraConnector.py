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

        # params
        self._params = []

        # payload
        self._payload = {
            'jsonrpc': '2.0',
            'id': 1,
        }

        # session
        self.session = requests.Session()
        self.session.headers.update({'User-agent':'InfuraConnector','Content-Type': 'application/json'})
        print(self.session.headers)

    def request(self,parameters):
        parameters.update({"jsonrpc":"2.0","id":1})

        r = self.session.post(url=self.base_url,json=parameters).json()

        # todo: handle with error
        # sample: {'jsonrpc': '2.0', 'id': 1, 'error': {'code': -32602, 'message': 'invalid argument 0: json: cannot unmarshal hex string of odd length into Go value of type common.Address'}}
        return r

    def eth_gasPrice(self):
        parameters = {'method': 'eth_gasPrice', "params": []}
        r = self.request(parameters)
        return int(r['result'], 16)
    
if __name__=="__main__":
    ic = InfuraConnector('16aef963ac304b66b9d697fb65d79806')
    print(ic.eth_gasPrice())
    