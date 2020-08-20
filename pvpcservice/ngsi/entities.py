import pandas as pd


def get_ngsi_v2_entity(df, id, first_ts, source="http://www.aemet.es/xml/municipios/localidad_46250.xml", timezone="Europe/Madrid", unit="EUR"):
    df['utc_iso_format'] = df['ts_end'].apply(pd.Timestamp.isoformat)
    entity_v2 = {
        "id": f"urn:ngsi-ld:Forecast:{id}",
        "type": "Forecast",
        "category": "EnergyPrice",
        "ObservedAt": {
            "value": pd.Timestamp.utcnow().tz_convert(timezone).floor('s').isoformat()
        },
        "dateIssued": {
            "value": first_ts.isoformat()
        },
        "source": {
            "value": source
        },
        "timezone": {
            "value": timezone
        },
        "indexes": {
            "value": df['utc_iso_format'].to_list(),
            "metadata": {
                "unitCode": {
                    "value": "ISO8601"
                }
            }
        },
        "values": {
            "value": df['price'].to_list(),
            "metadata": {
                "unitCode": {
                    "value": unit
                }
            }
        }
    }
    return entity_v2
