'''Helpful functions to clean data scraped from DoneDeal'''
import pandas
import re
import datetime as dt

today = dt.datetime.today()

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
def parse_engine(s:str)->float:
    search = re.search(r'(\d+\.\d+)\s*L',s,re.IGNORECASE)
    res:str = search.group(1) if search else 'nan'
    return float(res)
def parse_enginePower(s:str)->float:
    search = re.search(r'(\d+)\s*(hp|bhp)',s,re.IGNORECASE)
    res:str = search.group(1) if search else 'nan'
    return float(res)
def parse_acceleration(s:str)->float:
    search = re.search(r'(\d+\.?\d*)\s*sec',s,re.IGNORECASE)
    res:str = search.group(1) if search else 'nan'
    return float(res)
def parse_NCTExpiry(s:str)->int:
    dist = dt.datetime.strptime(s,'%b %Y')-today
    return dist.days
def encode_strings(column:pandas.Series)->pandas.DataFrame:
    '''
    given a pandas Series of strings, returns a dataframe where each unique string is mapped to a column of 1s and 0s

    for example:
    column = pd.Series(['a','b','a','c','b'])
    map_strings(column)
    returns:
       a  b  c
    0  1  0  0
    1  0  1  0
    2  1  0  0
    3  0  0  1
    4  0  1  0

    '''
    name:str          = column.name
    unique:list[str]  = column.unique().tolist()
    print(name)
    return column.apply(lambda variable:pandas.Series({f'{name}_is_{var}':1 if variable == var else 0 for var in unique}))