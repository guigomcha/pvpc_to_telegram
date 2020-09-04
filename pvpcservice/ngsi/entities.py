import pandas as pd


def get_ngsi_v2_entity(df, id, first_ts, provider="http://www.aemet.es/xml/municipios/localidad_46250.xml",
                       timezone="Europe/Madrid", unit="EUR/kWh", category="Deterministic"):
    """
    Provides a NGSI-v2 entity

    Args:
        df (pd.Dataframe): Expects columns ts_end and price describing a forecast
        id (str): Id of the entity. It will be appended to  the prefix "urn:ngsi-ld:Forecast:"
        first_ts (pd.Timestamp): Localtime z-aware ts describing the first timestamp from this the forecast applies
        provider (string): URl of the site that provided the forecast
        timezone (string): Region identification for the timezone
        unit (string): UnitCode for the forecast values
        category (string): Type of forecast ["Stochastic", "Deterministic", "Generic", "Others"]

    Returns (dict):
        NGSI-v2 entity
    """
    # TODO: Update to a Price Entity that is updated 24 time when the new prices are available
    df['utc_iso_format'] = df['ts_end'].apply(pd.Timestamp.isoformat)
    entity_v2 = {
        "id": f"urn:ngsi-ld:Forecast:{id}",
        "type": "Forecast",
        "category": category,
        "dateIssued": {
            "value": first_ts.isoformat()
        },
        "provider": {
            "value": provider
        },
        "timezone": {
            "value": timezone
        },
        "indexes": {
            "value": df['utc_iso_format'].to_list()
        },
        "values": {
            "value": df['price'].to_list()
        },
        "unitCode": {
            "value": unit
        }
    }
    return entity_v2
