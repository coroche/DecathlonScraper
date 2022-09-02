from decathlonScraper import notifyInstock
import googleSheetsAPI

def main():
    SCRIPT_ID = googleSheetsAPI.getScriptID()
    creds = googleSheetsAPI.login()
    service = googleSheetsAPI.buildService(creds)

    watchList = googleSheetsAPI.getActiveTrackers(SCRIPT_ID, service)

    for watch in watchList:
        _, instock = notifyInstock(watch[0], prodID = watch[1], combID = watch[2])
        if instock:
            googleSheetsAPI.removeWatch(SCRIPT_ID, service, watch[0], watch[1], watch[2])

if __name__ == '__main__':
    main()