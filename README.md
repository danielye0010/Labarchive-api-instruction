# Accessing LabArchives ELN Data via API in Python and R

This repository contains example code for calling selected LabArchives API endpoints from Python and R.

## Security Notice

The public repository does **not** include real credentials, user IDs, notebook IDs, signed API URLs, or downloaded notebook content. Use only accounts and notebooks you are authorized to access, and provide sensitive values through local environment variables.

Do not commit:

- access passwords or API keys;
- account passwords;
- user or notebook identifiers from restricted environments;
- signed request URLs;
- notebook exports or attachments containing restricted content.

## Workflow

### Step 1 — Retrieve authorized account and notebook metadata

Use the LabArchives `user_access_info` endpoint to retrieve the identifiers available to your authenticated account.

The Python and R examples read credentials from environment variables rather than embedding them in source code.

### Step 2 — Request a notebook backup

Use the `notebook_backup` endpoint with an authorized user ID and notebook ID. The request is signed using the LabArchives API authentication procedure.

A sanitized Python example is provided in `notebook backup.py`. It reads all identifiers and credentials locally and does not print the signed request URL.

## Suggested Environment Variables

```text
LABARCHIVES_EMAIL=
LABARCHIVES_PASSWORD=
LABARCHIVES_KEY_ID=
LABARCHIVES_ACCESS_PASSWORD=
LABARCHIVES_UID=
LABARCHIVES_NOTEBOOK_ID=
```

Use your institution's approved process to obtain API access. This repository intentionally does not document organization-specific credential distribution procedures.

## Notes

- Treat API responses as potentially sensitive.
- Store downloaded notebook backups outside the Git repository.
- Rotate or revoke credentials if you suspect they were exposed.
- Refer to the official LabArchives API documentation for current endpoint and authentication details.
