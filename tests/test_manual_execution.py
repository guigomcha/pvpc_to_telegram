import pytest
import json
from pathlib import Path

from pvpcservice.pvpc import PVPC


@pytest.mark.skip("Only for manual execution")
def test_manual_execution():
    manager = PVPC('TARIFALUZ')
    with open(Path.cwd() / Path('tokens.json')) as token_file:
        token_d = json.load(token_file)

    print(token_d)
    # tarifa luz scrapper don't need esios_ree_token
    token_d.pop('esios_ree_token')
    manager.alert_telegram(**token_d)