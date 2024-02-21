from django.urls import path

from bots.views import BotView

urlpatterns = [
    path('', BotView.as_view(), name='bot-list'),
    path('<int:bot_id>/', BotView.as_view(), name='bot-detail'),
]
