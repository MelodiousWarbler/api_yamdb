from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.views import (
    APIGetToken,
    APISignup,
    UsersViewSet,
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
    ReviewViewSet,
    CommentViewSet
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

router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns_auth = [
    path('signup/', APISignup.as_view(), name='signup'),
    path('token/', APIGetToken.as_view(), name='get_token'),
]

urlpatterns = [
    path('v1/auth/', include(urlpatterns_auth)),
    path('v1/', include(router_v1.urls)),
]
