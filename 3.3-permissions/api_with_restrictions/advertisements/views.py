from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    # TODO: настройте ViewSet, укажите атрибуты для кверисета,
    #   сериализаторов и фильтров
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvertisementFilter

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "update", "partial_update"]:
            return [IsAuthenticated()]
        return []

    def destroy(self, request, *args, **kwargs):
        """Удаление — только если пользователь является автором"""
        instance = self.get_object()
        if instance.creator != request.user:
            return Response(
                {"detail": "Вы не можете удалять чужие объявления."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)