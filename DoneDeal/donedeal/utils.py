import requests #type: ignore
import re
import json
from concurrent.futures import ThreadPoolExecutor
import pandas as pd

from .constants import (REQUEST_HEADERS,
                        CAR_HREF_PATTERN,
                        RESULTS_PER_PAGE,
                        NUM_CARS_PATTERN,
                        SOURCE_CODE_PATTERN)
from typing import Optional

def get_car_hrefs(url:str=None,urls:list[str]=None)->list[str]:
    '''
    given a dondeal search result url, return a list of car hrefs, scraped from that page.
    If multiple given, return a list of car hrefs scraped from all pages.
    '''
    if urls:
        res:list[str] = []
        with ThreadPoolExecutor() as executor:
            res = list(executor.map(get_car_hrefs,urls))
        return _concat_lists(*res)
    if url:
        res = requests.get(url,headers=REQUEST_HEADERS)
        return [href for href in CAR_HREF_PATTERN.findall(res.text) if not re.findall(r'\?campaign=\d+',href)]

def get_pageinated_urls(url:str)->list[str]:
    '''
    given a dondeal search result url, return a list of urls for each page.

    eg
    'https://www.donedeal.ie/cars' -> ['https://www.donedeal.ie/cars?start=0','https://www.donedeal.ie/cars?start=30',...]
    '''
    res = requests.get(url,headers=REQUEST_HEADERS)
    # pattern = re.compile(r'<h2 data-testid="h2-details-text" class="sc-[a-zA-Z\s]+"><span><strong>(\d[\d,\s]*)</strong><strong>cars </strong>in')
    num_cars:int = _parse_num_cars(NUM_CARS_PATTERN.findall(res.text),url)
    stop = num_cars//RESULTS_PER_PAGE
    url = url + '?' if '?' not in url else url + '&'
    return [url + f'start={i*RESULTS_PER_PAGE}' for i in range(stop+1)]

def get_json_data_from_ad_urls(hrefs:list[str],batch_size:int = 100)->list[dict]:
    '''
    Given a list of urls to an ad eg 'https://www.donedeal.ie/cars-for-sale/2021-audi-a3-1-0-tfs'
    
    1. get the html
    2. at the bottom of the html there is json, get it
    3. return a list of json dicts.

    batch_size is necessary as if there are a large number of urls requested initially, by the time the last request is made, the first request may have timed out.
    '''
    jsons = []
    batches = [hrefs[i:i+batch_size] for i in range(0,len(hrefs),batch_size)]
    for batch in batches:    
        with ThreadPoolExecutor() as executor:
            responses = list(executor.map(_make_request, batch))
            jsons += [_dict for _dict in list(executor.map(_get_json_from_src_code, responses)) if _dict]
        print("[{0}/{1}]".format(jsons.__len__(),hrefs.__len__()),end='\r')
    return jsons

def json_to_df(jsons:list[dict])->pd.DataFrame:
    '''
    given a list of json dicts, return a pandas dataframe
    '''
    records = []
    for _dict in jsons:
        displayAttributes = {_d['name']:_d['value'] for _d in _dict['props']['pageProps']['displayAttributes']}
        shallowAttrs = {k:v for k,v in _dict['props']['pageProps'].items() if not isinstance(v, (dict,list))}
        shallowAttrs.update(displayAttributes)

        res = pd.Series(shallowAttrs)
        records.append(res)
        
    return pd.DataFrame(records)

def _get_json_from_src_code(response:requests.models.Response)->dict[str]:
    if response is None:
        return None
    if response.status_code != 200:
        return None
    res = SOURCE_CODE_PATTERN.findall(response.text)
    _json = json.loads(res[0]) if res else None
    return _json

def _make_request(url:str)->requests.models.Response:
    '''make request with headers'''
    try:
        return requests.get(url, headers=REQUEST_HEADERS)
    except:
        return None
def _concat_lists(*args:list)->list:
    '''
    given a multiple lists, return a single list
    '''
    return [item for sublist in args for item in sublist]

def _parse_num_cars(num_cars:list[str],url:str)->int:
    '''
    given a list of strings, return the number of cars
    '''
    if not num_cars:
        print("No matches found, returning 0")
        return 0
    if num_cars.__len__() ==1:
        string = re.sub(r'\s|,', '', num_cars[0])
        return int(string)
    else:
        raise ValueError("Multiple matches found, revise code or look at html yourself. {filepath}".format(filepath=url))