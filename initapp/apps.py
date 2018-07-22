import os

from django.apps import AppConfig


class InitWebSocketsAppConfig(AppConfig):
    name = 'initapp'

    def ready(self):
        if not os.environ.get("ready_called"):
            from gettingstarted import followtask
            os.environ["ready_called"] = "1"
            followtask.start_web_socket.delay(2)
