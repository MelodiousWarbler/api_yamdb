from rest_framework import mixins, pagination, viewsets
from rest_framework.filters import SearchFilter

from api.permissions import isAdminOrReadOnly


class ListCreateDestroyViewSet(
    mixins.DestroyModelMixin, mixins.CreateModelMixin,
    mixins.ListModelMixin, viewsets.GenericViewSet
):
    permission_classes = (isAdminOrReadOnly,)
    pagination_class = pagination.LimitOffsetPagination
    lookup_field = 'slug'
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
