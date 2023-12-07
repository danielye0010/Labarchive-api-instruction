library(httr) # For making HTTP requests
library(digest) # For SHA1 and HMAC encoding
library(XML) # For parsing XML
library(base64enc) # For base64 encoding

# Set your ID
UID <- "36xxxxxxxxxxxxxxxxxxxxx" # Replace with actual UID
nbid1 <- "MTExxxxxxxxxxxxxxx=" # Replace with actual nbid1
nbid2 <- "MTEyyyyyyyyyyyyyyy=" # Replace with actual nbid2

# Set environment variables for credentials
key_id <- Sys.getenv('key_id')
access_password <- Sys.getenv('access_password')

# Get expire time
time_call <- paste0("https://api.labarchives.com/api/utilities/epoch_time?akid=", key_id)
time <- GET(time_call)
time_value <- content(time, "text")
time_xml <- xmlParse(time_value)
expires <- xmlValue(xmlRoot(time_xml)[[1]])

# Create new signature
sig_raw <- paste0(key_id, "notebook_backup", expires)
sig_byte <- charToRaw(sig_raw)
pass_byte <- charToRaw(access_password)
sig_digested <- hmac(pass_byte, sig_byte, algo = "sha1", raw = TRUE)
sig64 <- base64encode(sig_digested)
sig <- URLencode(sig64, reserved = TRUE)

# Construct the API call
call <- paste0("https://api.labarchives.com/api/notebooks/notebook_backup?uid=", UID, "&nbid=", nbid1) # Replace nbid1 with nbid2 for the second notebook

# Add auth parameters
auth <- paste0("&akid=", key_id, "&expires=", expires, "&sig=", sig)
api_call <- paste0(call, auth)

# Make the API call and download the notebook
r <- GET(api_call)
print(content(r, "text"))
