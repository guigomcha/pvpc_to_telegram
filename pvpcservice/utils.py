import bs4
import json
import logging
import matplotlib.pyplot as plt
import pandas as pd
import requests
from pathlib import Path

from loggingbot.loggingbot import TelegramBotHandler

def scrap_price_section():
    """
        Download prices for PVPC energy market. They should follow the https://schema.org/PriceSpecification reference.

    Returns (dict, {str: float}): Time interval to price value pairs. e.g {: } which indicates that
        from 00:00 to 01:00 energy costs is 0.1005 €

    """
    # Download page
    web = requests.get('https://tarifaluzhora.es/')
    web.raise_for_status()  # if error it will stop the program
    content = bs4.BeautifulSoup(web.text, 'html.parser')
    # Locate and format relevant info e.g '00h - 01h' and 0.1005
    ts_intervals = [i.text for i in content.findAll("span", {"itemprop": "description"})]
    price_per_interval = [eval(i.text.split(' ')[0]) for i in content.findAll("span", {"itemprop": "price"})]

    return _format(ts_intervals, price_per_interval)


def _format(ts_intervals, price_per_interval):
    def _ts_start_of_period(ts, delta):
        return (ts + pd.Timedelta(delta)).tz_localize(None).isoformat()

    date_observed = pd.Timestamp.utcnow().tz_convert("Europe/Madrid").floor('d')
    return {
        _ts_start_of_period(date_observed, interval.split(' ')[0]): price
        for interval, price in zip(ts_intervals, price_per_interval)
    }


def build_df(ts_to_price):
    # Format data
    return pd.DataFrame(ts_to_price, columns=['ts', 'price'])


def send_fig_to_telegram(df):
    with open(Path('tokens.json')) as f:
        tokens = json.load(f)
    logging.root.setLevel(logging.INFO)
    tbh = TelegramBotHandler(tokens['bot_token'], tokens['chats_token'])
    logging.root.addHandler(tbh)
    logger = logging.getLogger('pvpc_bot')

    # Format data and plot
    df.plot(x='ts', y='price', grid=True, kind='bar')
    plt.ylim(df['Price'].min(), df['Price'].max())
    plt.title('PVPC prices today in Spain')
    plt.xlabel('Time Interval Applicable')
    plt.ylabel('Price (€)')

    # Send the figure to Telegram
    logger.info('Extracting PVPC for energy in Spain', extra={'bot': True, 'figure': plt.gcf()})


def _add_color(df):
    # TODO: Find a way to have a color for each column based on its value
    import numpy as np
    cmap = plt.get_cmap('viridis')
    colors = cmap(np.linspace(0, 1, len(df['Price'].unique())))
    df['color'] = (df['Price'] / df['Price'].max())