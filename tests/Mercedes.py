import os,sys

where_am_i = os.path.dirname(os.path.abspath(__file__))
dd_path = os.path.join(where_am_i,'..','..')
print(dd_path)
sys.path.append(dd_path)

import pandas as pd
import plotly.express as px
from plotly.offline import plot
import DoneDeal as dd

#scraping
scraper = dd.CarScraper()
# search for Mercedes E-Class and BMW 3 Series in Ireland with mileage under 140,000km and price under 20,000
scraper.set_make_model(make='Mercedes-Benz',model='E-Class') 
scraper.set_make_model(make = 'BMW',model='3-Series')
scraper.set_mileage(mileage_to=140_000)
scraper.set_price(price_to=20_000)

scraper.set_arbitrary_kwargs(country='Ireland') #ignoring NI
print(scraper.url) #click the url to see the results for yourself
scraper.scrape(batch_size = 500) #batch_size is the amount of urls sent to TreadPoolExecutor at a time. Too little makes it slow, too much risks requests timing out.

#cleaning/formatting + features
df:pd.DataFrame = scraper.DataFrame.copy()[dd.constants.RECOMMENDED_COLUMNS] #alot of data gets returned, RECOMMENDED_COLUMNS is an optional subset of columns 

df=(df.pipe(dd.data_cleaning.assign_lat_lon) # turns string 'x,y' into (float(x),float(y))
      .pipe(dd.data_cleaning.assign_mileage) # turns string 'x km' or 'x mi' into float(x) in km (turns mi to km)
      .pipe(dd.data_cleaning.price_to_float)) # turns string 'abc,def' into float(abcdef)
df = (df.loc[lambda self:~self.price.apply(dd.data_cleaning.isBsPrice)] # drops prices like 1234,123456,123456789,111111111 etc 
        .loc[lambda self:~self.kilometers.apply(dd.data_cleaning.isBsPrice)])# sometimes the mileage is bs too. sequential digits like 123456 are just so unlikely 
df.year = df.year.astype(int)

#plot
fig = px.scatter_mapbox(df.dropna(subset='price'.split()),
                        lat='lat',
                        lon='lon',
                        color='make',
                        size='price',
                        hover_data=['make','model','price','kilometers','year','bodyType','transmission','friendlyUrl'],zoom=6)
fig.update_layout(mapbox_style="carto-darkmatter",height=1000,width=1200)
plot(fig)