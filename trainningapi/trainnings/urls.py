
from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import TrainingPointViewSet

r = DefaultRouter()
r.register('categories', views.CategoryViewSet, basename='category')
r.register('activities', views.ActivityViewSet, basename='activity')
r.register('participations', views.ParticipationViewSet, basename='participation')
r.register('users', views.UserViewSet, basename='user')
r.register('comments', views.CommentViewSet, basename='comment')
r.register('training-points', views.TrainingPointViewSet, basename='training-point')
r.register('missing-point-requests', views.MissingPointRequestViewSet, basename='missing_point_request')

urlpatterns = [
    path('', include(r.urls)),
    path('admin/training-points/export-pdf/',
         TrainingPointViewSet.as_view({'get': 'export_participation_pdf'}), name='export_training_points_pdf'),
]