import bs4
import requests

from pvpcservice import utils


class TarifaLuzHora:
    def __init__(self):
        self.source = 'https://tarifaluzhora.es/'

    def scrap(self, *args, **kwargs):
        """
        A scrapper class shall be able to return a dict with intervals to price value pairs  e.g {'0-1h': 0.1005}

        Returns (dict): interval_to_price

        """
        web = requests.get(self.source)
        web.raise_for_status()  # if error it will stop the program
        content = bs4.BeautifulSoup(web.text, 'html.parser')
        return self.process(content)

    @staticmethod
    def process(content):
        """
        Transforms a raw BeautifulSoup object into a dict of Time interval to price value pairs

        Args:
            content (BeautifulSoup object): parsed web page

        Returns (dict, {str: float}): e.g {'0-1h': 0.1005}
        """
        # Locate and format relevant info e.g '0-1h' and 0.1005
        ts_intervals = utils.ts_intervals()
        price_per_interval = [eval(i.text.split(' ')[0]) for i in content.findAll("span", {"itemprop": "price"})]

        return {
            interval.replace(':', ''): price for interval, price in zip(ts_intervals, price_per_interval)
        }
