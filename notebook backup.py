import base64
import hmac
import os
import urllib.parse
from hashlib import sha1

import requests
from xml.etree import ElementTree as ET

# Supply authorized credentials and notebook identifiers locally.
UID = os.environ.get("LABARCHIVES_UID")
NOTEBOOK_ID = os.environ.get("LABARCHIVES_NOTEBOOK_ID")
KEY_ID = os.environ.get("LABARCHIVES_KEY_ID")
ACCESS_PASSWORD = os.environ.get("LABARCHIVES_ACCESS_PASSWORD")

required = {
    "LABARCHIVES_UID": UID,
    "LABARCHIVES_NOTEBOOK_ID": NOTEBOOK_ID,
    "LABARCHIVES_KEY_ID": KEY_ID,
    "LABARCHIVES_ACCESS_PASSWORD": ACCESS_PASSWORD,
}
missing = [name for name, value in required.items() if not value]
if missing:
    raise RuntimeError(f"Missing required environment variables: {', '.join(missing)}")

# Obtain an expiration timestamp for the signed request.
time_call = f"https://api.labarchives.com/api/utilities/epoch_time?akid={KEY_ID}"
time_response = requests.get(time_call, timeout=30)
time_response.raise_for_status()
expires = ET.fromstring(time_response.text)[0].text

# Create the API signature without printing credentials or signed URLs.
sig_raw = f"{KEY_ID}notebook_backup{expires}".encode()
sig_digest = hmac.new(ACCESS_PASSWORD.encode(), sig_raw, digestmod=sha1).digest()
sig = urllib.parse.quote(base64.b64encode(sig_digest), safe="")

params = {
    "uid": UID,
    "nbid": NOTEBOOK_ID,
    "akid": KEY_ID,
    "expires": expires,
    "sig": sig,
}

response = requests.get(
    "https://api.labarchives.com/api/notebooks/notebook_backup",
    params=params,
    timeout=120,
)
response.raise_for_status()

# Save the authorized response locally. Do not commit downloaded notebook data.
with open("notebook_backup_response.bin", "wb") as output:
    output.write(response.content)
