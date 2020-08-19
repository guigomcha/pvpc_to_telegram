import bs4
import pandas as pd
import requests

from pvpcservice import utils


class PVPC:
    @staticmethod
    def _get_pvpc():
        # Download page
        date_observed = pd.Timestamp.utcnow().tz_convert("Europe/Madrid").floor('d')  # TODO: Query date
        web = requests.get('https://tarifaluzhora.es/')
        web.raise_for_status()  # if error it will stop the program
        content = bs4.BeautifulSoup(web.text, 'html.parser')
        interval_to_price = utils.scrap_price_section(content)
        return utils.build_df(date_observed, interval_to_price)

    def alert_telegram(self, bot_token, chats_token):
        df = self._get_pvpc()
        utils.send_fig_to_telegram(df, bot_token, chats_token)

    def get_pvpc_df(self):
        return self._get_pvpc()

    def get_ngsi_model(self):
        pass
