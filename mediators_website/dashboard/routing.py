from django.urls import re_path, path

from conflict import consumers

websocket_urlpatterns = [
    re_path(r'ws/dashboard/mediator/conflict-workplace/(?P<room_name>[A-Za-z0-9_-]+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/dashboard/user/conflict-workplace/(?P<room_name>[A-Za-z0-9_-]+)/$', consumers.ChatConsumer.as_asgi()),
]