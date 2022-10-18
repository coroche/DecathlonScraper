from pickle import FALSE, TRUE
import requests
from smtp import sendEmail


def parseURL(URL):
    URL = URL[0:URL.index(".html")+5]
    prodID = URL[URL.rindex("/")+1: URL.rindex("/")+7]
    combID = URL[URL.rindex("/")+8: URL.rindex("/")+14] 
    return prodID, combID
 
def getStock(prodID, combID):
    
    url = "https://www.decathlon.ie/modules/decastock/decastock-ajax.php?id_product=" + prodID + "&id_combination=" + combID

    r = requests.request("POST", url)
    data = r.json()

    stores = []
    if "stores" in data:
        for store in data["stores"]:
            if int(store["quantity"]) > 0:
                stores.append([store["name"], store["quantity"]])
    model = data["code_model"]
    return stores, data["master_quantity"], model

def getProductName(productID):
    url = "https://www.decathlon.ie/module/decaetlimporter/ajaxtitlerefresh?id_code_model=" + productID
    r = requests.request("POST", url)
    return r.text

def createMessage(instore, online, productName, prodID, combID, model):
    also = ",\n"
    
    if online == 1:
        are_is = "is "
    else:
        are_is = "are "
    
    messageTxt = ""
    link = "<a href=\"https://www.decathlon.ie/" + prodID + "-" + combID + ".html\">" + productName + "</a>"
    messageTxt += "There " + are_is + str(online) + " available online"
    if len(instore) == 0:
        messageTxt += "\nand 0 available instore"
    else:
        for i in range(len(instore)):
            if i == len(instore) - 1:
                also = "\nand "
            messageTxt += also + instore[i][1] + " available in " + instore[i][0]
    messageTxt += "."
    
    html = """\
<html>
  <body>
    <p>This item is now in stock.<br>""" + link + "<br><br>" + messageTxt.replace('\n', '<br>') +"""</p>
  </body>
</html>
"""
    return html, messageTxt


def notifyInstock(receiver_email, URL = '', prodID = '', combID = '', checkInStore = TRUE, checkOnline = TRUE):
    if not (prodID and combID) and URL:
        prodID, combID = parseURL(URL)
    elif not (prodID and combID) and not URL:
        return "provide product info", False
    
    instore, online, modelNo = getStock(prodID, combID)
    productName = getProductName(modelNo)
    html, messageTxt = createMessage(instore, online, productName, prodID, combID, modelNo)
    instock = False
    if (len(instore) and checkInStore) or (online > 0 and checkOnline):
        instock = True
        sendEmail(html, receiver_email, "Decathlon Stock Notification - " + productName)
    return messageTxt, instock


