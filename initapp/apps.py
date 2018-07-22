import os

from django.apps import AppConfig


class InitWebSocketsAppConfig(AppConfig):
    name = 'initapp'

    def ready(self):
        if not os.environ.get("ready_called"):
            os.environ["ready_called"] = "1"
            from users.models import User
            traders = User.objects.filter(role=User.TRADER)
            for trader in traders:
                print('DO WEBSOCKET STUFF!!!!!!!111')
                print(trader)
