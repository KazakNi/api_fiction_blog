from rest_framework import viewsets, filters
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAuthorOrReadOnly
from posts.models import Post, Group, Comment
from .serializers import (PostSerializer, GroupSerializer, CommentSerializer,
                          FollowSerializer)
from django.shortcuts import get_object_or_404


class PostViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAuthorOrReadOnly]
    pagination_class = LimitOffsetPagination

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAuthorOrReadOnly]

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        return post.comments

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post=post)


class GroupListRetrieveViewSet(mixins.ListModelMixin,
                               mixins.RetrieveModelMixin,
                               viewsets.GenericViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class FollowCreateListViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
        viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = FollowSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ('following__username',)

    def get_queryset(self):
        user = self.request.user
        return user.follower.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
