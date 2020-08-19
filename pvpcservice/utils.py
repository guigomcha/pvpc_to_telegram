import logging
import matplotlib.pyplot as plt
import pandas as pd


from loggingbot.loggingbot import TelegramBotHandler


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


def _format_timestamp(ts):
    """ Local Z-naive Timestamp. e.g 2020-08-19T00:00:00 """
    return ts.tz_localize(None)


def build_df(date_observed, interval_to_price):
    """
    Create a df based on scrapped values for further any

    Args:
        date_observed(pd.Timestamp): Local time Z-aware
        interval_to_price (dict, {str: float}): Time interval to price value pairs. e.g {'00h - 01h': 0.1005}

    Returns (pd.DataFrame):
        formatted prices to a df with ts_start, ts_end, interval and price columns
    """
    data = []
    for interval, price in interval_to_price.items():
        data.append({
            'ts_start': _format_timestamp(date_observed + pd.Timedelta(interval.split(' ')[0])),
            'ts_end': _format_timestamp(date_observed + pd.Timedelta(interval.split(' ')[-1])),
            'interval': interval,
            'price': price
        })
    return pd.DataFrame(data)


def send_fig_to_telegram(df, bot_token, chats_token):
    """
    Creates a plot for Time Interval to Price value and sends it to Telegram

    Args:
        df (pd.DataFrame): Expects ts and price columns
        bot_token (string): Telegram Bot token id
        chats_token (list of string): Telegram chat ids

    """
    # TODO: parametrise threshold for 'cheap' energy
    thr = 0.1
    logging.root.setLevel(logging.INFO)
    tbh = TelegramBotHandler(bot_token, chats_token)
    logging.root.addHandler(tbh)
    logger = logging.getLogger('pvpc_bot')
    today = df['ts_start'][0].date()
    degrees = 90
    # Format data and plot
    df_cheap = df[df['price'] < thr]
    df_expensive = df[df['price'] >= thr]

    plt.bar(df_cheap['interval'], df_cheap['price'], color='g')
    plt.bar(df_expensive['interval'], df_expensive['price'], color='r')
    plt.ylim(df['price'].min(), df['price'].max())
    plt.title(f'PVPC prices {today} in Spain')
    plt.xticks(rotation=degrees)
    plt.xlabel('Time Interval Applicable')
    plt.ylabel('Price (€)')
    plt.grid(True, axis='both')

    # Send the figure to Telegram
    logger.info(f'Extracting PVPC for energy in Spain for {today}', extra={'bot': True, 'figure': plt.gcf()})
