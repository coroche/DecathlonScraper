from decathlonScraper import notifyInstock
import googleSheetsAPI

SCRIPT_ID = googleSheetsAPI.getScriptID()
creds = googleSheetsAPI.login()
service = googleSheetsAPI.buildService(creds)

watchList = googleSheetsAPI.getActiveTrackers(SCRIPT_ID, service)

for watch in watchList:
    _, instock = notifyInstock(watch[0], watch[1])
    if instock:
        googleSheetsAPI.removeWatch(SCRIPT_ID, service, watch[0], watch[1])

# URL = 'https://www.decathlon.ie/mtb-cassettes/336743-120852-10-speed-11x48-cassette-adventx.html'
# eMail = 'comroche+decbot@gmail.com'

# notifyInstock(eMail, URL)