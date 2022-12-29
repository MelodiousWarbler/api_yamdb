from rest_framework import mixins, pagination, viewsets
from rest_framework.filters import SearchFilter

from api.permissions import IsAdminOrReadOnly


class ListCreateDestroyViewSet(
    mixins.DestroyModelMixin, mixins.CreateModelMixin,
    mixins.ListModelMixin, viewsets.GenericViewSet
):
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = pagination.LimitOffsetPagination
    lookup_field = 'slug'
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
