from django.urls import  re_path,path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/socket-server/(?P<room_name>\w+)/$',consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/game-master/(?P<room_name>\w+)/$',consumers.GameMaster.as_asgi()),
    re_path(r'ws/waiting-room/(?P<room_name>\w+)/$', consumers.SomeConsumer.as_asgi()),
    re_path(r'ws/task-updates/$', consumers.TaskWebSocketConsumer.as_asgi()),

]


http_routing = [
    re_path(r'^update_task/$', consumers.TaskHttpConsumer.as_asgi()),
]