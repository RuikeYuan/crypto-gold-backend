from app.serializers import (
    MetalSerializer
)

from app.utils.price import *
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny


class MetalViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]

    queryset = Metal.objects.all()
    serializer_class = MetalSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def fetch_all(self, request):
        # Implement metal price fetching logic here
        # You would typically use a metals price API
        pass