import json
from http import HTTPStatus

from pvpcservice.pvpc import PVPC


def telegram():
    try:
        PVPC().send_fig_to_telegram()
        return "Message Correctly sent to Telegram", HTTPStatus.OK
    except Exception as e:
        return f"Ups! There was a problem. {e}", HTTPStatus.INTERNAL_SERVER_ERROR


def prices():
    try:
        df = PVPC().get_pvpc_df()
        result = df.to_json(orient="columns")
        parsed = json.loads(result)
        response = json.dumps(parsed, indent=4)

        return f"{response}", HTTPStatus.OK
    except Exception as e:
        return "Ups! There was a problem", HTTPStatus.INTERNAL_SERVER_ERROR


def prices_v2():
    pass
if __name__ == "__main__":
    telegram()