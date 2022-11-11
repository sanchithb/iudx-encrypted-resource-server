import json
import base64
from nacl.public import SealedBox , PublicKey, PrivateKey
from iudx.rs.ResourceServer import ResourceServer
from iudx.rs.ResourceQuery import ResourceQuery

from typing import  List, Dict

from iudx.rs.ResourceResult import ResourceResult

from iudx.auth.Token import Token

import multiprocessing

temp_key_store = {}


class EncryptedResourceServer(ResourceServer):
    
    def __init__(self, rs_url: str=None, token: str=None, token_obj: Token=None,
                 headers: Dict[str, str]=None, publickey: str=None):
        
        super().__init__(rs_url, token, token_obj, headers)
        
        global temp_key_store 
        temp_key_store = self.key_gen()

        self.public_key = temp_key_store[1]
    
        self.headers[publickey]


    def key_gen():
        private_key = PrivateKey.generate()

        public_key = private_key.public_key

        return private_key, public_key

    def get_latest(self, queries: List[ResourceQuery]) -> List[ResourceResult]:

        super().get_latest(queries)

        ers_results = self.rs_results


