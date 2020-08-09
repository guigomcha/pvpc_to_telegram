import bs4
import requests


def scrap_price_section():
    """
        Download prices for PVPC energy market. They should follow the https://schema.org/PriceSpecification reference.

    Returns (dict, {str: float}): Time interval to price value pairs. e.g {'00h - 01h': 0.1005} which indicates that
        from 00:00 to 01:00 energy costs is 0.1005 €

    """
    # Download page
    web = requests.get('https://tarifaluzhora.es/')
    web.raise_for_status()  # if error it will stop the program
    content = bs4.BeautifulSoup(web.text, 'html.parser')
    # Locate and format relevant info
    ts_intervals = [i.text for i in content.findAll("span", {"itemprop": "description"})]
    price_per_interval = [eval(i.text.split(' ')[0]) for i in content.findAll("span", {"itemprop": "price"})]
    return {interval: price for interval, price in zip(ts_intervals, price_per_interval)}
