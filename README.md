# Decathlon Scraper
A web scraper to notify me when an item is in-stock in Decathlon.

Given a URL for an item on the decathlon.ie website, the quantity of stock is determined through an API call. If the item is instock, then an email notification is sent.
The checkDecathlonStock.bat file can be run with Windows Scheduler to poll the website on a schedule.

## To use
* Use the .env.example template to create a .env file with credentials for your sender email address.
* Edit decathlonScraper.py to include the URL of the product you are interested in and email address that you want to receive the notification to.
* Create a task on Windows Task Scheduler that runs checkDecathlonStock.bat as described [here](https://stackoverflow.com/questions/4437701/run-a-batch-file-with-windows-task-scheduler).