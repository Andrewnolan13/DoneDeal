get car listings from donedeal.ie

usage:

import DoneDeal as dd

# init scraping object
scraper = dd.CarScraper()
# search for Mercedes E-Class and BMW 3 Series in Ireland with mileage under 140,000km and price under 20,000
# this is just formatting the url
scraper.set_make_model(make='Mercedes-Benz',model='E-Class') 
scraper.set_make_model(make = 'BMW',model='3-Series')
scraper.set_mileage(mileage_to=140_000)
scraper.set_price(price_to=20_000)

# start scraping
scraper.scrape(batch_size=500)

# access scraped data
df = scraper.DataFrame #pandas.DataFrame
