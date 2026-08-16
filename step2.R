library(httr)
library(digest)
library(XML)
library(base64enc)

uid <- Sys.getenv("LABARCHIVES_UID")
notebook_id <- Sys.getenv("LABARCHIVES_NOTEBOOK_ID")
key_id <- Sys.getenv("LABARCHIVES_KEY_ID")
access_password <- Sys.getenv("LABARCHIVES_ACCESS_PASSWORD")

required <- c(
  LABARCHIVES_UID = uid,
  LABARCHIVES_NOTEBOOK_ID = notebook_id,
  LABARCHIVES_KEY_ID = key_id,
  LABARCHIVES_ACCESS_PASSWORD = access_password
)
if (any(required == "")) {
  stop("Missing required LabArchives environment variables.")
}

time_call <- paste0("https://api.labarchives.com/api/utilities/epoch_time?akid=", key_id)
time_response <- GET(time_call)
stop_for_status(time_response)
expires <- xmlValue(xmlRoot(xmlParse(content(time_response, "text")))[[1]])

sig_raw <- paste0(key_id, "notebook_backup", expires)
sig_digest <- hmac(charToRaw(access_password), charToRaw(sig_raw), algo = "sha1", raw = TRUE)
sig <- URLencode(base64encode(sig_digest), reserved = TRUE)

response <- GET(
  "https://api.labarchives.com/api/notebooks/notebook_backup",
  query = list(
    uid = uid,
    nbid = notebook_id,
    akid = key_id,
    expires = expires,
    sig = sig
  )
)
stop_for_status(response)

writeBin(content(response, "raw"), "notebook_backup_response.bin")
