import json
import base64

from nacl.public import SealedBox , PrivateKey

from iudx.rs.ResourceServer import ResourceServer
from iudx.rs.ResourceQuery import ResourceQuery
from iudx.rs.ResourceResult import ResourceResult
from iudx.auth.Token import Token

from typing import  List, Dict

private_key = PrivateKey.generate()

b_public_key = private_key.public_key.__bytes__()

# Encode the public key to base64

b64_b_public_key = base64.urlsafe_b64encode(b_public_key)

# Convert the encoded public key to string to send over http

str_b_public_key = b64_b_public_key.decode("utf-8")

class EncryptedResourceServer(ResourceServer):

    def decrypt(ers_results):
        
        ers_results = ers_results

        encrypted_data = ers_results[0].results

        # Decode the encrypted message from base64
        bytes_encrypted_data = base64.urlsafe_b64decode(encrypted_data)

        # Create a SealedBox object using Private Key
        unseal_box = SealedBox(private_key)

        # Decrypt the message by unsealed_box.decrypt()
        bytes_decrypted_data = unseal_box.decrypt(bytes_encrypted_data)

        # Decode to JSON format
        decrypted_data = json.loads(bytes_decrypted_data.decode('utf-8'))

        ers_results[0].results = decrypted_data
        
        return ers_results


    
    def __init__(self, rs_url: str=None, token: str=None, token_obj: Token=None,
                 headers: Dict[str, str]=None, publickey: str=None):
        
        super().__init__(rs_url, token, token_obj, headers)
        
        global temp_key_store 
        temp_key_store = self.key_gen()

        self.public_key = temp_key_store[1]
    
        self.headers[str_b_public_key]
        
    def get_latest(self, queries: List[ResourceQuery]) -> List[ResourceResult]:

        ers_results = super().get_latest(queries)
        drs_results = self.decrypt(ers_results)

        return drs_results
    
    def get_data(self, queries: List[ResourceQuery]) -> List[ResourceResult]:
        ers_results = super().get_data(queries)
        drs_results = self.decrypt(ers_results)

        return drs_results
