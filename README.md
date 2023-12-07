# Accessing LabArchives ELN Data via API in Python and R

This guide provides step-by-step instructions on accessing objects stored in an Electronic Lab Notebook (ELN) account through the LabArchives API using Python and R.

## Setup Environment Variables

Make sure you have all the variables ready, set the following environment variables for security:

- `access_password`: Your LabArchives access password. Ask UW-Madison ELN admin for it.
- `key_id`: Your LabArchives key ID. Ask  UW-Madison ELN admin for it.
- `password`: Your password from External Applications authentication at https://www.labarchives.com/.
- `email`: Your real NETID@WISC.EDU.

## Step 1: call "User Access Info" API to obtain the User ID (`UID`) and the Notebook ID (`nbid`) that you want to interact with.

## Step 2: call  "notebook_backup" API to download specific notebooks and their attachments from LabArchives in 7z zip format.
example call: https://<baseurl>/api/notebooks/notebook_backup?uid=0898098098800808&nbid=sdfjkshdfkjshdfkjhskdjfhskjdfh&<Call Authentication Parameters>
json  - (OPTIONAL) default is false; if 'true', notebook data returned in json format
no_attachments  - (OPTIONAL) default is false; if 'true', returned notebook data will not include attachments

## Notice:
Here two steps are seperated for easy understanding. If you want to programmaticly download your notebook, use library/package to read the XML. An example python code here:

import xml.etree.ElementTree as ET

xml_data = """
<response>
    <user>
        <uid>123456</uid>
        <notebooks>
            <notebook>
                <id>notebook_id_1</id>
            </notebook>
            <notebook>
                <id>notebook_id_2</id>
            </notebook>
        </notebooks>
    </user>
</response>
"""

root = ET.fromstring(xml_data)

uid = root.find('.//uid').text
print(f"UID: {uid}")

notebook_ids = root.findall('.//notebooks/notebook/id')
for nb_id in notebook_ids:
    print(f"Notebook ID: {nb_id.text}")

## Reference
For more detailed info, please visit labarchives api website:
https://mynotebook.labarchives.com/MzUuMXwyNy8yNy9Ob3RlYm9vay82NzcyMzY5MjN8ODkuMQ==/notebook-dashboard




