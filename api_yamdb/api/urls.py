from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.views import (
    APIGetToken,
    APISignup,
    UsersViewSet,
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet
)

app_name = 'api'

router_v1 = SimpleRouter()
router_v1.register(
    'users',
    UsersViewSet,
    basename='users'
)
router_v1.register(
    'categories',
    CategoryViewSet,
)
router_v1.register(
    'genres',
    GenreViewSet
)
router_v1.register(
    'titles',
    TitleViewSet
)

urlpatterns = [
    path('v1/auth/token/', APIGetToken.as_view(), name='get_token'),
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', APISignup.as_view(), name='signup'),
]