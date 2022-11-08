from iudxe2ee import EncryptedResourceServer

from iudx.rs.ResourceServer import ResourceServer
from iudx.rs.ResourceQuery import ResourceQuery

# entity id for the pune env aqm sensor.
entity_id = "datakaveri.org/04a15c9960ffda227e9546f3f46e629e1fe4132b/rs.iudx.org.in/pune-env-aqm/f36b4669-628b-ad93-9970-f9d424afbf75"

sent_key = open('publickey.key', 'r').read()

# creating an object of ResourceServer class using rs_url.
ers = EncryptedResourceServer.ers(
         rs_url="https://rs.iudx.org.in/ngsi-ld/v1",
         headers={"content-type": "application/json"},
         key=sent_key
     )

# printing results
print(f"RESULTS: {ers[0]}")        # get the result data of the resource query.
print(f"STATUS: {ers[1]}")            # get the status code for the response.