from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import MethodNotAllowed

from posts.models import Group, Post, Comment
from .serializers import GroupSerializer, PostSerializer, CommentSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def create(self, request, *args, **kwargs):
        raise MethodNotAllowed('Method POST not allowed!')


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def update(self, request, *args, **kwargs):
        user = self.request.user
        post = self.get_object()
        if user != post.author:
            return Response(
                {'Detail': 'You do not have permission to perform'
                 'this action.'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        user = self.request.user
        post = self.get_object()
        if user != post.author:
            return Response(
                {'Detail': 'You do not have permission to perform'
                 'this action.'},
                status=status.HTTP_403_FORBIDDEN
            )

        return super().destroy(request, *args, **kwargs)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs['post_pk']
        return Comment.objects.filter(post_id=post_id)

    def perform_create(self, serializer):
        post_id = self.kwargs['post_pk']
        post = Post.objects.get(id=post_id)
        serializer.save(
            author=self.request.user,
            post=post
        )

    def update(self, request, *args, **kwargs):
        user = self.request.user
        post = self.get_object()
        if user != post.author:
            return Response(
                {'Detail': 'You do not have permission to perform'
                 'this action.'},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = CommentSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            post_id = self.kwargs['post_pk']
            post = Post.objects.get(id=post_id)
            serializer.save(
                author=self.request.user,
                post=post
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return super().destroy(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        user = self.request.user
        post = self.get_object()
        if user != post.author:
            return Response(
                {'Detail': 'You do not have permission to perform'
                 'this action.'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)
