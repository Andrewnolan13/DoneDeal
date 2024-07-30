'''Helpful functions to clean data scraped from DoneDeal'''
import pandas
import re

def assign_lat_lon(df:pandas.DataFrame)->pandas.DataFrame:
    '''Assigns latitude and longitude to a dataframe'''
    df['lat lon'.split()]=df.geoPoint.str.extract(r'([+-]?\d+\.\d+),\s*([+-]?\d+\.\d+)').rename(columns={0:'lat',1:'lon'}).astype(float)
    df.drop(columns='geoPoint',inplace=True)
    return df
def assign_mileage(df:pandas.DataFrame)->pandas.DataFrame:
    df[['clockedDistance','unit']] = df.mileage.str.replace(r',','').str.extract(r'([,\d]*)\s*(km|mi)').rename(columns={0:'clockedDistance',1:'unit'})
    df['clockedDistance'] = df.clockedDistance.astype(float)
    df['kilometers'] = (df.unit == 'km')*df.clockedDistance + (df.unit == 'mi')*df.clockedDistance*1.60934
    df['kilometers'] = (df.kilometers<1000)*df.kilometers*1000 + df.kilometers*(df.kilometers>=1000)
    df.drop(columns=['mileage','clockedDistance','unit'],inplace=True)
    return df
def price_to_float(df:pandas.DataFrame)->pandas.DataFrame:
    df.price = df.price.apply(lambda x: re.sub(r'[^\d]','',x) if isinstance(x,str) else x).astype(float)
    return df
def isBsPrice(x:float)->bool:
    '''There are a lot of ads on donedeal with prices like 123456789 etc. This function returns True if the price is a bs price'''
    if x==0 or x >=1_000_000:
        return True
    s=str(x)
    if s.isalpha(): #eg nan, NaN, None etc
        return False
    bullshit:bool = True
    for idx,ch in enumerate(re.sub(r'\.\d*','',s)):
        bullshit *= int(ch) == idx+1
    return bullshit==1