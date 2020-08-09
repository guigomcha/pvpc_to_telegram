import json
import logging
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

from loggingbot.loggingbot import TelegramBotHandler
from pvpcscrapper.pvpcscrapper import scrap_price_section

if __name__ == '__main__':
    with open(Path('tokens.json')) as f:
        tokens = json.load(f)
    logging.root.setLevel(logging.INFO)
    tbh = TelegramBotHandler(tokens['bot_token'], tokens['chats_token'])
    logging.root.addHandler(tbh)
    logger = logging.getLogger('pvpc_bot')
    # Scrap prices from PVPC web page
    interval_to_price = scrap_price_section()

    # Format data and plot
    df = pd.DataFrame({'Price': list(interval_to_price.values()), 'Interval': list(interval_to_price.keys())})
    df.plot(x='Interval', y='Price', grid=True, kind='bar')
    plt.ylim(df['Price'].min(), df['Price'].max())
    plt.title('PVPC prices today in Spain')
    plt.xlabel('Time Interval Applicable')
    plt.ylabel('Price (€)')

    # Send the figure to Telegram
    logger.info('Extracting PVPC for energy in Spain', extra={'bot': True, 'figure': plt.gcf()})


def _add_color():
    # TODO: Find a way to have a color for each column based on its value
    import numpy as np
    cmap = plt.get_cmap('viridis')
    colors = cmap(np.linspace(0, 1, len(df['Price'].unique())))
    df['color'] = (df['Price'] / df['Price'].max())