import pandas as pd
import matplotlib.pyplot as plt


def build_df(date_issued, interval_to_price):
    """
    Create a df based on scrapped values for further processing

    Args:
        date_issued(pd.Timestamp): Local time Z-aware
        interval_to_price (dict, {str: float}): Time interval to price value pairs. e.g {'0-1h': 0.1005}

    Returns (pd.DataFrame):
        formatted prices to a df with ts_start, ts_end, interval and price columns
    """
    data = []
    for interval, price in interval_to_price.items():
        data.append({
            'ts_start': date_issued + pd.Timedelta(interval.split('-')[0]+'h'),
            'ts_end': date_issued + pd.Timedelta(interval.split('-')[-1]),
            'interval': interval,
            'price': price
        })
    return pd.DataFrame(data)


def today(tz_name):
    return pd.Timestamp.utcnow().tz_convert(tz_name).floor('d')


def tomorrow(tz_name):
    _today = today(tz_name)
    return _today + pd.Timedelta(days=1)


def format_df_and_save_to_file(df):
    # TODO: parametrize threshold for 'cheap' energy
    thr1 = 0.1
    thr2 = 0.11
    today = df['ts_start'][0].date()
    degrees = 90
    # Format data and plot
    df_cheap = df[df['price'] < thr1]
    df_in_between = df[(df['price'] >= thr1) & (df['price'] < thr2)]
    df_expensive = df[df['price'] >= thr2]
    plt.bar(df_cheap.index, df_cheap['price'], color='g')
    plt.bar(df_in_between.index, df_in_between['price'], color='y')
    plt.bar(df_expensive.index, df_expensive['price'], color='r')
    plt.ylim(df['price'].min(), df['price'].max())
    plt.title(f'PVPC prices {today} in Spain')
    plt.xticks(ticks=range(len(df)), labels=df['interval'].values, rotation=degrees)
    plt.xlabel('Time Interval Applicable')
    plt.ylabel('Price (€)')
    plt.grid(True, axis='both')
    plt.savefig('prices_plot.png', bbox_inches='tight')
    plt.clf()
    return 'prices_plot.png'


def ts_intervals():
    return [f"{i}-{i+1}h" for i in range(24)]