import re

DOMAIN="https://www.donedeal.co.uk"
CARURL = "{}/cars".format(DOMAIN)
REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
}
CAR_HREF_PATTERN = re.compile(r'li data-testid="listing-card-index-\d+" class="sc-[a-zA-Z\s]+"><a href="(/cars-for-sale/[^"]+)"')
NUM_CARS_PATTERN = re.compile(r'<h2 data-testid="h2-details-text" class="sc-[a-zA-Z\s]+"><span><strong>(\d[\d,\s]*)</strong>')
SOURCE_CODE_PATTERN = re.compile(r'<script id="__NEXT_DATA__" type="application/json" crossorigin="anonymous">(\{.*\})</script>')
RECOMMENDED_COLUMNS = 'make model price fuelType trim transmission engine enginePower acceleration seats numDoors colour country owners roadTax NCTExpiry bodyType year mileage currency sellerType county countyTown geoPoint header description friendlyUrl'.split()
RESULTS_PER_PAGE = 30