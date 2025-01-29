
from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter
from . import views

r = DefaultRouter()
r.register('categories', views.CategoryViewSet, basename='cate')
r.register('activities', views.ActivityViewSet, basename='activity')
r.register('participations', views.ParticipationViewSet, basename='participation')
r.register('users', views.UserViewSet, basename='user')
r.register('comments', views.CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(r.urls))
]