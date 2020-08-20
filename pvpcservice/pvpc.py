import bs4
import logging
import matplotlib.pyplot as plt
import pandas as pd
import requests

from loggingbot.loggingbot import TelegramBotHandler

from pvpcservice.ngsi import entities
from pvpcservice import utils


class PVPC:
    def __init__(self):
        self.entity_id = "EnergyPricePVPC1"
        self.source = 'https://tarifaluzhora.es/'
        self.tz = "Europe/Madrid"

    @property
    def today(self):
        return pd.Timestamp.utcnow().tz_convert(self.tz).floor('d')

    def _get_pvpc_df(self):
        # Download page
        date_issued = self.today  # TODO: Query date
        web = requests.get(self.source)
        web.raise_for_status()  # if error it will stop the program
        content = bs4.BeautifulSoup(web.text, 'html.parser')
        interval_to_price = utils.scrap_price_section(content)
        return utils.build_df(date_issued, interval_to_price)

    def alert_telegram(self, bot_token, chats_token):
        """
        Creates a plot for Time Interval to Price value and sends it to Telegram

        Args:
            bot_token (string): Telegram Bot token id
            chats_token (list of string): Telegram chat ids

        """
        df = self._get_pvpc_df()
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

    def get_ngsi_v2_model(self):
        """
        Obtains forecasts and returns back an NGSI-v2 complaint entity
        Returns:

        """
        df = self._get_pvpc_df()
        entity = entities.get_ngsi_v2_entity(df, self.entity_id, self.today)
        return entity
