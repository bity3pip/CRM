from rest_framework import generics
from apps.accounts.models import User
from .serializers import ChatterMetricSerializer
from .permissions import IsTeamlead


class ChatterMetricsView(generics.ListAPIView):
    serializer_class = ChatterMetricSerializer
    permission_classes = [IsTeamlead]

    def get_queryset(self):
        return (
            User.objects
            .filter(role=User.Role.CHATTER)
            .prefetch_related('chatter_dialogs')
        )