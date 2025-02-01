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
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import HttpResponse

import csv
from django.http import JsonResponse
from django.core.files.storage import default_storage
from rest_framework.parsers import MultiPartParser


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
        participation = self.get_object()

        if request.method.__eq__('POST'):
            content = request.data.get('content')
            c = Comment.objects.create(content=content, user=request.user, participation=participation)

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
    parser_classes = [MultiPartParser]

    @action(detail=False, methods=['post'], url_path='upload-csv')
    def upload_csv(self, request):
        file = request.FILES.get('file')

        if not file.name.endswith('.csv'):
            return JsonResponse({'error': 'Not CSV file!'}, status=400)

        file_path = default_storage.save(f'uploads/{file.name}', file)

        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                user = User.objects.filter(username=row['username']).first()
                activity = Activity.objects.filter(title=row['activity']).first()
                point = int(row['point'])

                if user and activity:
                    TrainingPoint.objects.update_or_create(
                        user=user, activity=activity,
                        defaults={'point': point, 'criteria': '1'}
                    )

        return JsonResponse({'success': 'List have been update!'})

    @action(methods=['get'], url_path='export-pdf', detail=False)
    def export_participation_pdf(self, request):
        training_point = TrainingPoint.objects.all()

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="training_points.pdf"'

        p = canvas.Canvas(response, pagesize=letter)
        width, height = letter

        p.setFont("Helvetica-Bold", 16)
        p.drawString(100, height - 40, "Training Point List")

        p.setFont("Helvetica", 12)
        y = height - 80
        p.drawString(80, y, "ID")
        p.drawString(150, y, "Student's Name")
        p.drawString(350, y, "Activity")
        p.drawString(450, y, "Point")
        p.drawString(550, y, "Achievement")

        y -= 20
        for tp in training_point:
            if y < 100:
                p.showPage()
                y = height - 40
            p.drawString(80, y, str(tp.id))
            p.drawString(150, y, tp.user.username)
            p.drawString(300, y, tp.activity.title)
            p.drawString(450, y, str(tp.point))
            p.drawString(550, y, tp.achievement)
            y -= 20

        p.showPage()
        p.save()

        return response

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
