import json
from http import HTTPStatus

from pvpcservice.pvpc import PVPC


def telegram(access_info):
    try:
        PVPC().alert_telegram(access_info['bot_token'], access_info['chats_token'])
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
        return f"Ups! There was a problem. {e}", HTTPStatus.INTERNAL_SERVER_ERROR


def prices_v2():
    pass

# if __name__ == "__main__":
#     access_info = {
#       "bot_token": "1361411284:AAHmT2mlcpAW9RNiZ3D7fe8rgwsdH_W-5xY",
#       "chats_token": ["-438788913"]
#     }
#     telegram(access_info)