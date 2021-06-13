from pathlib import Path

import telebot

from pvpcservice import utils
from pvpcservice.ngsi import entities
from pvpcservice.esios_ree_scrapper import EsiosRee
from pvpcservice.tarifa_luz_hora_scrapper import TarifaLuzHora


class PVPC:
    def __init__(self, scrapper, tz_name="Europe/Madrid", esios_token=""):
        """

        Args:
            scrapper (ENUM): Available options are ESIOS or TARIFA
            tz_name (string): name of the timezone
            esios_token (string): Required if scrapper=ESIOS
        """
        self.tz = tz_name
        self.entity_id = "EnergyPricePVPC1"
        self.scrapper = EsiosRee(esios_token) if scrapper == "ESIOS" else TarifaLuzHora()

    def alert_telegram(self, bot_token, chats_token):
        """
        Creates a plot for Time Interval to Price value and sends it to Telegram

        Args:
            bot_token (string): Telegram Bot token id
            chats_token (list of string): Telegram chat ids

        """
        df = self.get_df()
        file_name = utils.format_df_and_save_to_file(df)
        # Send the figure to Telegram
        bot = telebot.TeleBot(bot_token)
        bot.send_photo(chats_token[0], photo=open(file_name, 'rb'))
        Path(file_name).unlink()

    def get_ngsi_v2_model(self):
        """
        Obtains forecasts and returns back an NGSI-v2 complaint entity

        Returns (dict):
            NGSI-v2 model describing the forecast. Full schema in pvpcservice/ngsi/schema.json

        """
        df = self.get_df()
        entity = entities.get_ngsi_v2_entity(df, self.entity_id, utils.today(self.tz))
        return entity

    def get_df(self):
        interval_to_price = self.scrapper.scrap()
        # ESIOS return a day in advance
        request_day = utils.today(self.tz) if isinstance(self.scrapper, TarifaLuzHora) else utils.tomorrow(self.tz)
        df = utils.build_df(request_day, interval_to_price)
        return df
