from decathlonScraper import notifyInstock
import googleSheetsAPI

def main():
    SCRIPT_ID = googleSheetsAPI.getScriptID()
    creds = googleSheetsAPI.login()
    service = googleSheetsAPI.buildService(creds)

    watchList = googleSheetsAPI.getActiveWatchers(SCRIPT_ID, service)

    for watch in watchList:
        _, instock = notifyInstock(watch[0], prodID = watch[1], combID = watch[2], checkInStore = watch[3], checkOnline = watch[4])
        if instock:
            googleSheetsAPI.removeWatch(SCRIPT_ID, service, watch[0], watch[1], watch[2], watch[3], watch[4])

if __name__ == '__main__':
    main()