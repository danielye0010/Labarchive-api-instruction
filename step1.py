import base64
import hmac
import os
import urllib.parse
from hashlib import sha1
from xml.etree import ElementTree as ET

import requests

EMAIL = os.environ.get("LABARCHIVES_EMAIL")
PASSWORD = os.environ.get("LABARCHIVES_PASSWORD")
KEY_ID = os.environ.get("LABARCHIVES_KEY_ID")
ACCESS_PASSWORD = os.environ.get("LABARCHIVES_ACCESS_PASSWORD")

required = {
    "LABARCHIVES_EMAIL": EMAIL,
    "LABARCHIVES_PASSWORD": PASSWORD,
    "LABARCHIVES_KEY_ID": KEY_ID,
    "LABARCHIVES_ACCESS_PASSWORD": ACCESS_PASSWORD,
}
missing = [name for name, value in required.items() if not value]
if missing:
    raise RuntimeError(f"Missing required environment variables: {', '.join(missing)}")

time_response = requests.get(
    f"https://api.labarchives.com/api/utilities/epoch_time?akid={KEY_ID}",
    timeout=30,
)
time_response.raise_for_status()
expires = ET.fromstring(time_response.text)[0].text

sig_raw = f"{KEY_ID}user_access_info{expires}".encode()
sig_digest = hmac.new(ACCESS_PASSWORD.encode(), sig_raw, digestmod=sha1).digest()
sig = urllib.parse.quote(base64.b64encode(sig_digest), safe="")

params = {
    "login_or_email": EMAIL,
    "password": PASSWORD,
    "akid": KEY_ID,
    "expires": expires,
    "sig": sig,
}

response = requests.get(
    "https://api.labarchives.com/api/users/user_access_info",
    params=params,
    timeout=30,
)
response.raise_for_status()

# Inspect the response locally to identify authorized user/notebook IDs.
# Avoid committing API responses containing account or notebook metadata.
print(response.text)
