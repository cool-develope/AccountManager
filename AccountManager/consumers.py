from channels.generic.websocket import WebsocketConsumer
import json
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf.urls import url

class AccountConsumer(WebsocketConsumer):
    def connect(self):
        self.message_type = self.scope['url_route']['kwargs']['message_type']
        self.group_name = 'report_%s' % (self.message_type)

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type': 'send_message',
                'message': message
            }
        )

    # Receive message from room group
    def send_message(self, event):
        message = event['message']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))

websocket_urlpatterns = [
    url(r'^ws/report/(?P<message_type>[^/]+)/$', AccountConsumer),
]

application = ProtocolTypeRouter({
    'websocket': URLRouter(
            websocket_urlpatterns
        )
})

def send_rebalance_report(message):
    channel_layer = get_channel_layer()
    route = 'report_rebalance'
    async_to_sync(channel_layer.group_send)(
        route, {
            "type": "send_message",
            "message": message,
        }
    )

def send_account_report(account):
    channel_layer = get_channel_layer()
    message = "%d;%.5f;%.5f;%.5f;%.5f;%.2f;%.5f;%.5f" % (account.id, account.balance, account.margin, account.free_margin, account.equity, account.open_lots, account.profit, account.swap_profit)
 
    route = 'report_account'
    async_to_sync(channel_layer.group_send)(
        route, {
            "type": "send_message",
            "message": message,
        }
    )

def send_log(message):
    channel_layer = get_channel_layer() 
    route = 'report_log'
    async_to_sync(channel_layer.group_send)(
        route, {
            "type": "send_message",
            "message": message,
        }
    )