from pathlib import Path
import bs4

from pvpcservice.tarifa_luz_hora_scrapper import TarifaLuzHora


def test_scrap():
    # Cannot run between 00:00 and 02:00 since the web is not updated
    scrapper = TarifaLuzHora()
    intervals_to_price_d = scrapper.scrap()
    assert isinstance(intervals_to_price_d, dict)
    assert len(intervals_to_price_d) == 24
    assert '00h - 01h' in intervals_to_price_d.keys()


def test_process():
    scrapper = TarifaLuzHora()
    with open(Path.cwd() / Path('resources', 'beautiful_soup.txt')) as file:
        content = file.read()
    content = bs4.BeautifulSoup(content, 'html.parser')
    intervals_to_price_d = scrapper.process(content)
    assert isinstance(intervals_to_price_d, dict)
    assert len(intervals_to_price_d) == 24
    assert '00h - 01h' in intervals_to_price_d.keys()
