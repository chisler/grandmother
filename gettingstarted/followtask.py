import hashlib
import hmac
import time
import websocket

import django
from celery import shared_task
from celery.utils.log import get_task_logger
import os

from kombu.utils import json

from external.exchange_api import ExternalExchange
from subscription.models import Subscription
from users.models import User

import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gettingstarted.settings')

logger = get_task_logger(__name__)

global current_trader

# This is the decorator which a celery worker uses

import time, threading


def pong_periodic(ws):
    pong(ws)
    threading.Timer(1, lambda: pong_periodic(ws)).start()


def login(ws, API_SECRET, API_KEY):
    nonce = int(time.time() * 1000000)
    auth_payload = 'AUTH{}'.format(nonce)
    signature = hmac.new(
        API_SECRET.encode(),
        msg=auth_payload.encode(),
        digestmod=hashlib.sha384
    ).hexdigest()

    payload = {
        'apiKey': API_KEY,
        'event': 'auth',
        'authPayload': auth_payload,
        'authNonce': nonce,
        'authSig': signature
    }

    ws.send(json.dumps(payload))


def on_message(ws, message, current_trader):
    logger.info(message)
    message = json.loads(message)
    if message[1] == "te":
        for subscriotion in Subscription.objects.filter(user_followed=current_trader):
            investor = subscriotion.follower
            amount = message[2][4]
            currency = message[2][1]
            currency = currency[:3] + '/' + currency[3:] + 'T'
            logger.info(amount)
            logger.info(currency)
            if amount > 0:
                ExternalExchange(investor.api_key, investor.secret_key).market_order_buy(currency,
                                                                                         subscriotion.initial_ratio * amount)
            else:
                ExternalExchange(investor.api_key, investor.secret_key).market_order_sell(currency,
                                                                                          subscriotion.initial_ratio * (
                                                                                                  0 - amount))


def on_error(ws, error):
    logger.info(error)


def on_close(ws, current_trader):
    logger.info("### closed ###")
    initSocket(current_trader)


def on_open(ws, current_trader):
    logger.info("### open ###")
    login(ws, current_trader.secret_key, current_trader.api_key)
    pong(ws)


def pong(ws):
    payload = {
        "event": "ping"
    }
    ws.send(json.dumps(payload))


@shared_task(name="start_web_socket")
def start_web_socket(traderId):
    websocket.enableTrace(True)
    initSocket(User.objects.filter(id=traderId).first())


def initSocket(current_trader):
    ws = websocket.WebSocketApp('wss://hackathon.ethfinex.com/ws/',
                                on_message=lambda ws, message: on_message(ws, message, current_trader),
                                on_error=on_error,
                                on_close=lambda ws: on_close(ws, current_trader))
    ws.on_open = lambda ws: on_open(ws, current_trader)
    ws.run_forever()
