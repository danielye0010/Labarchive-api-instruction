library(httr) # For making HTTP requests
library(digest) # For SHA1 and HMAC encoding
library(XML) # For parsing XML
library(base64enc) # For base64 encoding

# Set credentials (ensure these environment variables are set in your R environment)
access_password <- Sys.getenv('access_password') # ask UW-Madison ELN admin for it
key_id <- Sys.getenv('key_id') # ask UW-Madison ELN admin for it
password <- Sys.getenv('password') # copy from External Applications authentication
email <- Sys.getenv('email') # copy from External Applications authentication

# Get expire time
time_call <- paste0("https://api.labarchives.com/api/utilities/epoch_time?akid=", key_id)
time <- GET(time_call)
time_value <- content(time, "text")
time_xml <- xmlParse(time_value)
expires <- xmlValue(xmlRoot(time_xml)[[1]])

# Create signature
sig_raw <- paste0(key_id, "user_access_info", expires)
sig_byte <- charToRaw(sig_raw)
pass_byte <- charToRaw(access_password)
sig_digested <- hmac(pass_byte, sig_byte, algo = "sha1", raw = TRUE)
sig64 <- base64encode(sig_digested)
sig <- URLencode(sig64, reserved = TRUE)

# Base call
base_call <- paste0("https://api.labarchives.com/api/users/user_access_info?login_or_email=", email, "&password=", password)

# Auth
auth <- paste0("&akid=", key_id, "&expires=", expires, "&sig=", sig)
api_call <- paste0(base_call, auth)

# Call
r <- GET(api_call)
print(content(r, "text"))


