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
## Install:
To clone the repository and run the test script, follow these steps:

1. Open the command prompt.
2. Navigate to the directory where you want to clone the repository. Use the following commands:
```
cd C:\path\to\desired\location
git clone https://github.com/Andrewnolan13/DoneDeal.git
```
## Test:
After the repository is cloned, navigate to the `DoneDeal/tests` directory and run `Mercedes.py`:
```
cd DoneDeal/tests
python Mercedes.py
```
This will execute the `Mercedes.py` script and display a plot in your browser.
![alt text](media/plot.png)
<!-- ![alt text](media/plot.html) -->
### Built-in Data cleaning functions:
```python
#cleaning/formatting + features
df:pd.DataFrame = scraper.DataFrame.copy()
df=df[dd.constants.RECOMMENDED_COLUMNS] #alot of data gets returned, RECOMMENDED_COLUMNS is an optional subset of columns 

df=(df.pipe(dd.data_cleaning.assign_lat_lon) # turns string 'x,y' into (float(x),float(y))
      .pipe(dd.data_cleaning.assign_mileage) # turns string 'x km' or 'x mi' into float(x) in km (turns mi to km)
      .pipe(dd.data_cleaning.price_to_float)) # turns string 'abc,def' into float(abcdef)
df = (df.loc[lambda self:~self.price.apply(dd.data_cleaning.isBsPrice)] # drops prices like 1234,123456,123456789,111111111 etc 
        .loc[lambda self:~self.kilometers.apply(dd.data_cleaning.isBsPrice)])# sometimes the mileage is bs too. sequential digits like 123456 are just so unlikely 
```


