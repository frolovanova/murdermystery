from django.urls import path
from . import views


urlpatterns = [
    path('',views.title),
    path('chat/<str:game_code>/<str:character>/<str:chatee>/',views.lobby),
    path('home/<str:game_code>/<str:character_name>/', views.home, name='home'),
    path('characters/<str:game_code>/<str:selectedCharacter>/',views.characters),
    path('checklist/<str:game_code>/<str:character>/', views.checklist),
    path('new_game/', views.new_game, name='new_game'),
    path('waiting/', views.waiting_room, name='waiting_room'),
    path('update_waiting_room/', views.update_waiting_room, name='update_waiting_room'),
    path('test/',views.home),
    path('act1/<str:game_code>/<str:character>/',views.act1),

    path('end/<str:game_code>/<str:character>/',views.end),

    path('u/<str:game_code>/', views.update_game_state, name='update_game_state')
]