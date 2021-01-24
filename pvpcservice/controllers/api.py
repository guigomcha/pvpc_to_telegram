from http import HTTPStatus

from pvpcservice.pvpc import PVPC


def telegram(access_info):
    """
    Main endpoint for the app.

    Args:
        access_info (dict): Expected tokens for the Bot ('bot_token' str) and the group/channel
         ('chats_token' list of str)

    Returns (tuple of str, int):
        Normal Request-type response

    """
    try:
        PVPC().alert_telegram(access_info['bot_token'], access_info['chats_token'])
        return "Message Correctly sent to Telegram", HTTPStatus.OK
    except Exception as e:
        return f"Ups! There was a problem. {e}", HTTPStatus.INTERNAL_SERVER_ERROR


def prices_v2():
    """ Additional endpoint to retrieve prices in NGSI-V2 format """
    try:
        response = PVPC().get_ngsi_v2_model()
        return f"{response}", HTTPStatus.OK
    except Exception as e:
        return f"Ups! There was a problem. {e}", HTTPStatus.INTERNAL_SERVER_ERROR

