from celery import shared_task
from celery.utils.log import get_task_logger
import websocket
from psycopg2._json import Json

try:
    import thread
except ImportError:
    import _thread as thread


logger = get_task_logger(__name__)


# This is the decorator which a celery worker uses

def on_message(ws, message):
    logger.info(message)

def on_error(ws, error):
    logger.info(error)

def on_close(ws):
    logger.info("### closed ###")

def on_open(ws):
    logger.info("### open ###")



@shared_task(name="send_feedback_email_task")
def send_feedback_email_task():
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://api.bitfinex.com/ws/",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()
