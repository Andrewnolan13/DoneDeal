'''
CarScraper should be simple. The arguments should be the url arguments used to filter the search.
'''
from pandas import DataFrame
from types import NoneType
from typing import Literal

from .constants import CARURL
from . import utils

class CarScraper:
    def __init__(self)->None:
        self.url = CARURL
        self._num_filters = 0

    def _inc_num_filters(self)->None:
        if self._num_filters == 0:
            self.url += '?'
        self._num_filters += 1
    
    def _format_url_arg(self,arg:str)->str:
        if self._num_filters == 0:
            char = "?"
        else:
            char = "&"
        self._num_filters += 1
        return f"{char}{arg}"
    
    def _raiseArgError(self,**kwargs:dict)->None:
        '''raises error if all kwargs are None'''
        for v in kwargs.values():
            if v:
                return None
        raise ValueError("At least one argument must be provided")
    
    def _raiseIntervalError(self,**kwargs)->None:
        key1,key2 = kwargs.keys()
        from_,to_ = kwargs.values()
        if from_ and to_ and from_ > to_:
            raise ValueError(f"{key1} must be <= {key2}")
        
    def set_make_model(self, make:str,model:str|NoneType=None)->None:
        self.url += self._format_url_arg(f"make={make}"+(f";model:{model}" if model else ""))

    def set_year(self, year_from:int|NoneType=None, year_to:int|NoneType=None)->None:
        self._raiseArgError(year_from=year_from,year_to=year_to)
        self._raiseIntervalError(year_from=year_from,year_to=year_to)
        self.url += self._format_url_arg(f"year_from={year_from}") if year_from else ""
        self.url += self._format_url_arg(f"year_to={year_to}") if year_to else ""

    def set_price(self, price_from:int|NoneType=None, price_to:int|NoneType=None)->None:
        self._raiseArgError(price_from=price_from,price_to=price_to)
        self._raiseIntervalError(price_from=price_from,price_to=price_to)
        self.url += self._format_url_arg(f"price_from={price_from}") if price_from else ""
        self.url += self._format_url_arg(f"price_to={price_to}") if price_to else ""

    def set_mileage(self, mileage_from:int|NoneType=None, mileage_to:int|NoneType=None)->None:
        self._raiseArgError(mileage_from=mileage_from,mileage_to=mileage_to)
        self._raiseIntervalError(mileage_from=mileage_from,mileage_to=mileage_to)
        self.url += self._format_url_arg(f"mileage_from={mileage_from}") if mileage_from else ""
        self.url += self._format_url_arg(f"mileage_to={mileage_to}") if mileage_to else ""

    def set_area(self, area:str,countyTown:str|NoneType=None,radius:int=25)->None:
        self.url += self._format_url_arg(f"area={area}")
        self.url += self._format_url_arg(f"countyTown={countyTown}") if countyTown else ""
        self.url += self._format_url_arg(f"radius={radius}")
    
    def set_seller(self, seller:Literal['pro','private'])->None:
        if seller not in ['pro','private']:
            raise ValueError("seller must be 'pro' or 'private'")
        self.url += self._format_url_arg(f"sellerType={seller}")
    
    def scrape(self,batch_size:int = 100)->None:
        pageinated_search_urls:list[str] = utils.get_pageinated_urls(self.url)
        self.hrefs:list[str] = ['https://www.donedeal.ie'+href for href in utils.get_car_hrefs(urls=pageinated_search_urls)]
        print("retrieved {0} urls matching your criteria".format(self.hrefs.__len__()))
        self.json:list[dict] = utils.get_json_data_from_ad_urls(self.hrefs,batch_size=batch_size)
        print("retrieved {0} jsons".format(self.json.__len__()))
        self.DataFrame:DataFrame = utils.json_to_df(self.json)
        print("converted jsons to DataFrame")