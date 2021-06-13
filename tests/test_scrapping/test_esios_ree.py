import json
from pathlib import Path

from pvpcservice.esios_ree_scrapper import EsiosRee


def test_process():
    scrapper = EsiosRee("")
    with open(Path.cwd() / Path('resources', 'esios_ree_indicators_response.json')) as file:
        content = json.load(file)
    intervals_to_price_d = scrapper.process(content)
    assert isinstance(intervals_to_price_d, dict)
    assert len(intervals_to_price_d) == 24
    assert '00h - 01h' in intervals_to_price_d.keys()