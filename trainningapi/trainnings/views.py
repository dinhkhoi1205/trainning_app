from gc import get_objects
from pickle import FALSE

from django.shortcuts import render
from django.template.context_processors import request
from rest_framework import viewsets, generics, permissions
from rest_framework.response import Response
from trainnings import serializers, paginator
from trainnings.models import (Category, Activity,
                               Participation, User, Comment, TrainingPoint, MissingPointRequest)
from rest_framework.decorators import action
from trainnings import perms


# Create your views here.
class CategoryViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer


class ActivityViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Activity.objects.filter(active=True)
    serializer_class = serializers.ActivitySerializer
    pagination_class = paginator.ItemPaginator
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [permissions.IsAdminUser()]  # Only admin or assistant
        return [permissions.AllowAny()]

    def get_queryset(self):
        query = self.queryset

        cate_id = self.request.query_params.get('category_id')
        if cate_id:
            query = query.filter(category_id=cate_id)

        kw = self.request.query_params.get('q')
        if kw:
            query = query.filter(title__icontains=kw)

        return query

    @action(methods=['get'], url_path='participation', detail=True)
    def get_participation(self, request, pk):
        participation = self.get_object().participation_set.filter(is_attended=True)

        return Response(
            serializers.ParticipationSerializer(participation, many=True, context={'request': request}).data)


class ParticipationViewSet(viewsets.ViewSet, generics.RetrieveAPIView):
    queryset = Participation.objects.all()
    serializer_class = serializers.ParticipationDetailsSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy', 'get_comments']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    @action(methods=['get', 'post'], url_path='comments', detail=True)
    def get_comments(self, request, pk):
        if request.method.__eq__('POST'):
            content = request.data.get('content')
            c = Comment.objects.create(content=content, user=request.user, participation=get_objects())

            return Response(
                serializers.CommentSerializer(c).data)
        else:
            comments = self.get_object().comment_set.select_related('user').filter(active=True)

            return Response(
                serializers.CommentSerializer(comments, many=True).data)


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = serializers.UserSerializer

    def get_permissions(self):
        if self.action in ['update', 'destroy']:
            return [permissions.IsAdminUser()]  # Only admin
        return [permissions.AllowAny()]

    @action(methods=['get'], url_path='current-user', detail=False, permission_classes=[permissions.IsAuthenticated])
    def get_user(self, request):
        return Response(serializers.UserSerializer(request.user, context={'request': request}).data)


class CommentViewSet(viewsets.ViewSet, generics.DestroyAPIView):
    queryset = Comment.objects.filter(active=True)
    serializer_class = serializers.CommentSerializer
    permission_classes = [perms.OwnerPerms]

    def get_permissions(self):
        if self.action in ['create']:
            return [permissions.IsAuthenticated()]
        return [perms.OwnerPerms()]


class TrainingPointViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = TrainingPoint.objects.all()
    serializer_class = serializers.TrainingPointSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return TrainingPoint.objects.all()  # Only admin can see point
        return TrainingPoint.objects.filter(user=user)  # Only student can see their own point


class MissingPointRequestViewSet(viewsets.ViewSet, generics.ListCreateAPIView):
    queryset = MissingPointRequest.objects.all()
    serializer_class = serializers.MissingPointRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return MissingPointRequest.objects.all()  # Admin see all request
        return MissingPointRequest.objects.filter(user=user)  # Student can see their own request
