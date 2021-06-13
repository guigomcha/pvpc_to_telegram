import pandas as pd

from pvpcservice.utils import build_df


def test_build_df():
    interval_to_price = {'00h - 01h': 0.1, '01h - 02h': 0.2}
    date_issued = pd.Timestamp('2021-01-24T00:00:00Z')
    expected_df = pd.DataFrame({
            'ts_start': [pd.Timestamp('2021-01-24T00:00:00Z'), pd.Timestamp('2021-01-24T01:00:00Z')],
            'ts_end': [pd.Timestamp('2021-01-24T01:00:00Z'), pd.Timestamp('2021-01-24T02:00:00Z')],
            'interval': ['00h - 01h', '01h - 02h'],
            'price': [0.1, 0.2]
        })
    df = build_df(date_issued, interval_to_price)
    assert df.equals(expected_df)


