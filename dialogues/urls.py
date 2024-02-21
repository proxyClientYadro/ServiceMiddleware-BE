from django.urls import path

from dialogues.views import DialoguesView, MessagesView

urlpatterns = [
    path('', DialoguesView.as_view(), name='dialogue-list'),
    path('<int:dialogue_id>/', DialoguesView.as_view(), name='dialogue-operations'),
    path('<int:dialogue_id>/messages/', MessagesView.as_view(), name='message-operations'),
]
