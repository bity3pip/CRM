from django.urls import path
from .views import (DialogListView, MessageListView,
                    SendMessageView, FanMessageView,
                    read_dialog
                    )

urlpatterns = [
    path('dialogs/', DialogListView.as_view(), name='dialog-list'),
    path('dialogs/<int:dialog_id>/messages/',
         MessageListView.as_view(),
         name='message-list'
         ),
    path('dialogs/<int:dialog_id>/messages/send/',
         SendMessageView.as_view(),
         name='send-message'
         ),
    path('dialogs/<int:dialog_id>/fan-message/',
         FanMessageView.as_view(),
         name='fan-message'
         ),
    path('dialogs/<int:dialog_id>/read/',
         read_dialog,
         name='read-dialog'
         ),
]
