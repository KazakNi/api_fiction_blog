from django.urls import path, include
from rest_framework import routers
from .views import (PostViewSet, GroupListRetrieveViewSet, CommentViewSet,
                    FollowCreateListViewSet)

router = routers.DefaultRouter()
router.register('posts', PostViewSet)
router.register('groups', GroupListRetrieveViewSet)
router.register(r'posts/(?P<post_id>[1-9]\d*)/comments', CommentViewSet)
router.register('follow', FollowCreateListViewSet, basename='following')

urlpatterns = [
    path('v1/', include(router.urls)),
]
