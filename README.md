Get car listings from donedeal.ie

## Usage:

```python
import DoneDeal as dd

# Initialize scraping object
scraper = dd.CarScraper()

# Search for Mercedes E-Class and BMW 3 Series in Ireland with mileage under 140,000km and price under 20,000
# This is just formatting the search URL
scraper.set_make_model(make='Mercedes-Benz', model='E-Class') 
scraper.set_make_model(make='BMW', model='3-Series')
scraper.set_mileage(mileage_to=140_000)
scraper.set_price(price_to=20_000)

# Start scraping
scraper.scrape(batch_size=500)

# Access scraped data
df = scraper.DataFrame  # pandas.DataFrame
```
