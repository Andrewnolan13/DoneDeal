import requests
from . import (core,
                constants,
                utils,
                data_cleaning)

scraper = core.CarScraper()

res = requests.get(scraper.url,headers=constants.REQUEST_HEADERS)
num_cars:int = utils._parse_num_cars(constants.NUM_CARS_PATTERN.findall(res.text),scraper.url)

def main():
    print(f'{num_cars} cars in Ireland')

if __name__ == '__main__':
    main()