# paste your ID
UID = "36xxxxxxxxxxxxxxxxxxxxx"
nbid1 = "MTExxxxxxxxxxxxxxx="
nbid2 = "MTEyyyyyyyyyyyyyyy="
UID = os.environ.get('UID')
key_id = os.environ.get('key_id')
access_password = os.environ.get('access_password')

# expire
time_call = "https://api.labarchives.com/api/utilities/epoch_time?akid=" + key_id
time = requests.get(time_call)
time = time.text
root = ET.fromstring(time)
expires = root[0].text

# new sig
sig_raw = key_id + "notebook_backup" + expires
sig_byte = bytearray(sig_raw.encode())
pass_byte = bytearray(access_password.encode())
sig_digested = hmac.new(pass_byte, sig_byte, digestmod=sha1).digest()
sig64 = base64.b64encode(sig_digested)
sig = urllib.parse.quote(sig64, safe='')

call = "https://api.labarchives.com/api/notebooks/notebook_backup" + "?uid=" + UID + "&nbid=" + nbid

# auth
auth = "&akid=" + key_id + "&expires=" + expires + "&sig=" + sig
api_call = call + auth

# download notebook and its attachment in 7z zip file
r = requests.get(api_call)

