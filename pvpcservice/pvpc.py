from pvpcservice import utils


class PVPC:
    @staticmethod
    def _get_pvpc_df():
        content = utils.scrap_price_section()
        return utils.build_df(content)

    def send_fig_to_telegram(self):
        df = self._get_pvpc_df()
        utils.send_fig_to_telegram(df)

    def get_pvpc_df(self):
        return self._get_pvpc_df()

    def get_ngsi_model(self):
        pass
