import pandas as pd


def scrap_price_section(content):
    """
    Download prices for PVPC energy market. They should follow the https://schema.org/PriceSpecification reference.

    Args:
        content (BeautifulSoup object): parsed web page

    Returns (dict, {str: float}): Time interval to price value pairs. e.g {'00h - 01h': 0.1005}
    """
    # Locate and format relevant info e.g '00h - 01h' and 0.1005
    ts_intervals = [i.text for i in content.findAll("span", {"itemprop": "description"})]
    price_per_interval = [eval(i.text.split(' ')[0]) for i in content.findAll("span", {"itemprop": "price"})]

    return {
        interval.replace(':', ''): price for interval, price in zip(ts_intervals, price_per_interval)
    }


def build_df(date_issued, interval_to_price):
    """
    Create a df based on scrapped values for further any

    Args:
        date_issued(pd.Timestamp): Local time Z-aware
        interval_to_price (dict, {str: float}): Time interval to price value pairs. e.g {'00h - 01h': 0.1005}

    Returns (pd.DataFrame):
        formatted prices to a df with ts_start, ts_end, interval and price columns
    """
    data = []
    for interval, price in interval_to_price.items():
        data.append({
            'ts_start': date_issued + pd.Timedelta(interval.split(' ')[0]),
            'ts_end': date_issued + pd.Timedelta(interval.split(' ')[-1]),
            'interval': interval,
            'price': price
        })
    return pd.DataFrame(data)

