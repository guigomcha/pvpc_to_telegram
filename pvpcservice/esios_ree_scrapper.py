import requests


class EsiosRee:
    def __init__(self, token):
        self.token = token
        self.source = 'https://api.esios.ree.es/indicators'
        # GeoID: 8741 - Peninsula, 8742 - Canarias, 8743 - Baleares, 8744 - Ceuta, 8745 - Melilla
        self.geo_id = 8741
        # Indicator info
        """
        {
            'name': 'Término de facturación de energía activa del PVPC 2.0TD',
             'description': '<p>Precio horario del t&eacute;rmino de energ&iacute;a que se aplican en la factura el&eacute;ctrica de los consumidores con una potencia contratada no superior a 15 kW y que est&eacute;n acogidos al PVPC (Precio Voluntario para el Peque&ntilde;o Consumidor).</p><p>Incluye el t&eacute;rmino de energ&iacute;a de los peajes de acceso, los cargos y el coste de producci&oacute;n. No incluye impuestos.</p><p><b>Publicaci&oacute;n:</b> diariamente a las 20:20 horas con la informaci&oacute;n del d&iacute;a D+1.</p>',
             'id': 1001
        }
        """
        self.indicator = 1001
        self.headers = {
            'Accept': 'application/json; application/vnd.esios-api-v2+json',
            'Content-Type': 'application/json',
            'Host': 'api.esios.ree.es',
            'Authorization': f'Token token=\"{self.token}\"'
        }

    def scrap(self):
        """
        A scrapper class shall be able to return a dict with intervals to price value pairs  e.g {'00h - 01h': 0.1005}

        Returns (dict): interval_to_price

        """
        response = requests.get(self.source, headers=self.headers)
        response.raise_for_status()
        return self.process(response.json())

    def process(self, content):
        """
        Transforms a json object from ESIOS REE into a dict of Time interval to price value pairs

        Args:
            content (BeautifulSoup object): parsed web page

        Returns (dict, {str: float}): e.g {'00h - 01h': 0.1005}
        """
        # List received in order from 00:00 to 00:00 of the next day
        ts_intervals = [f"{self.format_hour(i)} - {self.format_hour(i+1)}" for i in range(24)]
        price_per_interval = []
        for value_d in content['indicator']['values']:
            if value_d['geo_id'] != self.geo_id:
                continue
            price_per_interval.append(value_d['value'])
        return {
            interval: price for interval, price in zip(ts_intervals, price_per_interval)
        }

    @staticmethod
    def format_hour(hour):
        return f"0{hour}h" if len(str(hour)) == 1 else f"{hour}h"