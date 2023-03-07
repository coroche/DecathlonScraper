# Decathlon Scraper
A web scraper to send notifications when an item is in stock in Decathlon.

Submit your email and the url of a decathlon.ie product [here](https://coroche.github.io/decabot/) and recieve an email when it is in stock. 

A python programme is scheduled to run every hour. The programme first connects to the form response sheet via Google Cloud APIs and retrieves a list of unique emails and product codes. It then loops through these records checking stock via API calls to Decathlon. If the item is instock, a notification email is sent and the record is removed from the response sheet. This is currently deployed on a Raspberry Pi to run uninterrupted.
