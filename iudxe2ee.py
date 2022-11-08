# pip install pynacl

import json
import base64
from nacl.public import SealedBox , PublicKey
from iudx.rs.ResourceServer import ResourceServer
from iudx.rs.ResourceQuery import ResourceQuery

# base class
class EncryptedResourceServer():
    
    def ers(self, rs_url, headers, key, entity_id):
        # taking the parameters passed to the class
        self.rs_url = rs_url
        self.headers = headers
        self.key = key
        self.entity_id = entity_id

        # creating an object of ResourceServer class using rs_url.

        rs = ResourceServer(
         rs_url=self.rs_url,
         headers=self.headers
        )

        # creating a query for fetching latest data for the entity_id.
        rs_query = ResourceQuery()
        rs_entity = rs_query.add_entity(entity_id)

        # fetch results for a list of entities.
        results = rs.get_latest([rs_entity])

        # store the result type in a variable
        result_type = results[0].type

        # store the result data in a variable to be further encrypted
        message = results[0].results

        # take the public key passed

        str_b_public_key = self.key

        # Decode it from base64

        b64_b_public_key = base64.urlsafe_b64decode(str_b_public_key)

        # convert the bytes to object type

        public_key = PublicKey(b64_b_public_key)

        # Create a SealedBox object

        sealed_box = SealedBox(public_key)

        # Convert the JSON data to bytes
        message_bytes = json.dumps(message).encode()

        encrypted = sealed_box.encrypt(message_bytes)

        # encrypted is of type bytes and it is not JSON Serializable
        # We convert it to string and send it

        b64_encrypted = base64.urlsafe_b64encode(encrypted)

        str_encrypted = b64_encrypted.decode("utf-8")

        encrypted_result = {
            "results":[
                {
                    "Encrypted Data": [str_encrypted]
                }
            ]
        }

        return encrypted_result, result_type

    

        