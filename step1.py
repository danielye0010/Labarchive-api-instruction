import os
from hashlib import sha1  # for encoding the signature
import hmac  # for encoding the signature
import base64  # for encoding the signature
import urllib  # for "percent" aka url encoding
import requests  # for getting response from API
import xml.etree.ElementTree as ET  # for reading XML output of API response

# set credentials as environment variables for security

access_password = os.environ.get('access_password')  # ask UW-Madison ELN admin for it
key_id = os.environ.get('key_id')  # ask UW-Madison ELN admin for it
password = os.environ.get('password')  # copy from External Applications authentication
email = os.environ.get('email')  # copy from External Applications authentication

# expire
time_call = "https://api.labarchives.com/api/utilities/epoch_time?akid=" + key_id
time = requests.get(time_call)
time = time.text
root = ET.fromstring(time)
expires = root[0].text

# sig
sig_raw = key_id + "user_access_info" + expires
sig_byte = bytearray(sig_raw.encode())
pass_byte = bytearray(access_password.encode())
sig_digested = hmac.new(pass_byte, sig_byte, digestmod=sha1).digest()
sig64 = base64.b64encode(sig_digested)
sig = urllib.parse.quote(sig64, safe='')

# base call
base_call = "https://api.labarchives.com/api/users/user_access_info?login_or_email=" + email + "&password=" + password

# auth
auth = "&akid=" + key_id + "&expires=" + expires + "&sig=" + sig
api_call = base_call + auth

# call
r = requests.get(api_call)
# record your UID and NotebookID which you want to download from the output
print(r.text)

# example output
# <users>
#  <id>36xxxxxxxxxxxxxxxxxxxxx</id>
# < notebook >
# < id > MTExxxxxxxxxxxxxxxxxxxxxx=< / id >
# < name > My Notebook 1< / name >
# < notebook >
# < id > MTExxxxxxxxxxxxxxxxxxxxxx=< / id >
# < name > My Notebook 2< / name >

