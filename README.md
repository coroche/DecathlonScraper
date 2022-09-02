# Decathlon Scraper
A web scraper to send notifications when an item is in stock in Decathlon.

Submit your email and the url of a decathlon.ie product [here](https://forms.gle/p8gz56N8cfCN86t8A) and recieve an email when it is in stock. 

A python programme is called by a batch file running on a schedule. The programme first connects to the form response sheet via Google Cloud APIs and retrieves a list of unique emails and product codes. It then loops through these records checking stock via API calls to Decathlon. If the item is instock, a notification email is sent and the record is removed from the response sheet.
