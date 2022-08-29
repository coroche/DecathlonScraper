import requests
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

port = os.getenv('port')
smtp_server = os.getenv('smtp_server')
sender_email = os.getenv('sender_email') 
password = os.getenv('password')  

def parseURL(URL):
    URL = URL[0:URL.index(".html")+5]
    prodID = URL[URL.rindex("/")+1: URL.rindex("/")+7]
    combID = URL[URL.rindex("/")+8: URL.rindex("/")+14] 
    return prodID, combID
 
parseURL("https://www.decathlon.ie/mtb-cassettes/336743-120852-10-speed-11x48-cassette-adventx.html")   

def getStock(prodID, combID):
    
    instock = False
    url = "https://www.decathlon.ie/modules/decastock/decastock-ajax.php?id_product=" + prodID + "&id_combination=" + combID

    r = requests.request("POST", url)
    data = r.json()

    stores = []
    if "stores" in data:
        for store in data["stores"]:
            if int(store["quantity"]) > 0:
                instock = True
                stores.append([store["name"], store["quantity"]])
    instock = instock or (int(data["master_quantity"]) > 0)
    model = data["code_model"]
    return stores, data["master_quantity"], instock, model

def getProductName(productID):
    url = "https://www.decathlon.ie/module/decaetlimporter/ajaxtitlerefresh?id_code_model=" + productID
    r = requests.request("POST", url)
    return r.text

def createMessage(instore, online, URL, model):
    also = ""
    messageTxt = ""
    productName = getProductName(model)
    messageTxt += "<a href=\"" + URL + "\">" + productName + "</a>"
    messageTxt += "\nThere are " + str(online) + " available online"
    if len(instore) == 0:
        messageTxt += "\nand 0 available instore"
    else:
        for i in range(len(instore)):
            if i == len(instore) - 1:
                also = "and "
            messageTxt +="\n" + also + instore[i][1] + " available in " + instore[i][0]

    html = """\
<html>
  <body>
    <p>""" + messageTxt.replace('\n', '<br>') +"""</p>
  </body>
</html>
"""
    return MIMEText(html, "html"), messageTxt

def sendEmail(html, port, smtp_server, sender_email, receiver_email, password):
    message = MIMEMultipart()
    message["Subject"] = "Decathlon Stock Notification"
    message["From"] = sender_email
    message["To"] = receiver_email
    message.attach(html)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())

def notifyInstock(URL, receiver_email):
    prodID, combID = parseURL(URL)
    instore, online, instock, modelNo = getStock(prodID, combID)
    html, messageTxt = createMessage(instore, online, URL, modelNo)
    if instock:
        sendEmail(html, port, smtp_server, sender_email, receiver_email, password)
    return messageTxt

