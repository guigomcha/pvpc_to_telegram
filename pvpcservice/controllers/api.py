import json
from http import HTTPStatus

from pvpcservice.pvpc import PVPC


def telegram(access_info):
    try:
        PVPC().alert_telegram(access_info['bot_token'], access_info['chats_token'])
        return "Message Correctly sent to Telegram", HTTPStatus.OK
    except Exception as e:
        return f"Ups! There was a problem. {e}", HTTPStatus.INTERNAL_SERVER_ERROR


def prices_v2():
    try:
        response = PVPC().get_ngsi_v2_model()
        return f"{response}", HTTPStatus.OK
    except Exception as e:
        return f"Ups! There was a problem. {e}", HTTPStatus.INTERNAL_SERVER_ERROR
