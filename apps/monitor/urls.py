from django.urls import path
from .views import ChatterMetricsView

urlpatterns = [
    path('monitor/chatters/',
         ChatterMetricsView.as_view(),
         name='chatter-metrics'),
]
