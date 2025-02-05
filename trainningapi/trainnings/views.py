from collections import defaultdict
from rest_framework import viewsets, generics, permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from trainnings import serializers, paginator
from trainnings.models import (Category, Activity,
                               Participation, User, Comment, TrainingPoint, MissingPointRequest,Register)
from rest_framework.decorators import action
from trainnings import perms
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import HttpResponse

import csv

from trainnings.serializers import RegisterSerializer, RegisterCheckSerializer


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

    @action(methods=['get'], url_path='export-csv', detail=False)
    def export_csv(self, request):
        participations = Participation.objects.filter(is_attended=True)

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="all_activities_participations.csv"'

        writer = csv.writer(response)

        writer.writerow(['Activity ID', 'Activity Title', 'User ID', 'Username', 'Class', 'Faculty', 'Points'])

        for participation in participations:
            training_point = TrainingPoint.objects.filter(user=participation.user).first()

            row = [
                participation.activity.id,
                participation.activity.title,
                participation.user.id,
                participation.user.username,
                training_point.class_name if training_point else "N/A",
                training_point.faculty.name if training_point and training_point.faculty else "N/A",
                participation.point if participation.point else "N/A"
            ]
            writer.writerow(row)

        return response


class ParticipationViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Participation.objects.filter(active=True)
    serializer_class = serializers.ParticipationSerializer
    pagination_class = paginator.ItemPaginator
    permission_classes = [permissions.IsAuthenticated]


class ActivityDetailsViewSet(viewsets.ViewSet, generics.RetrieveAPIView):
    queryset = Activity.objects.prefetch_related('tags').filter(active=True)
    serializer_class = serializers.ActivityDetailsSerializer

    def get_permissions(self):
        if self.action in ['get_comments'] and self.request.method in ['POST']:
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    @action(methods=['GET', 'POST'], url_path='comments', detail=True)
    def get_comments(self, request, pk):
        if request.method.__eq__('POST'):
            content = request.data.get('content')
            c = Comment.objects.create(content=content, user=request.user, activity=self.get_object())

            return Response(serializers.CommentSerializer(c).data)
        else:
            comments = self.get_object().comment_set.select_related('user').filter(active=True)

            return Response(serializers.CommentSerializer(comments, many=True).data)

    @action(methods=['post', 'get'], detail=True, url_path='register')
    def register_activity(self, request, pk):
        activity = self.get_object()
        if request.method == 'POST':
            register = activity.register_set.create(user=request.user)
            return Response(RegisterSerializer(register).data, status=status.HTTP_201_CREATED)

        if request.method == 'GET':
            query = Register.objects.filter(activity=activity, user=request.user)

            if query.exists():
                return Response(RegisterCheckSerializer(query, many=True).data)

            if query.exists():
                return Response(RegisterCheckSerializer(query, many=True).data)

            return Response([{"status": 0}])


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

    @action(methods=['get'], url_path='export-pdf', detail=False)
    def export_participation_pdf(self, request):
        training_points = TrainingPoint.objects.select_related('user', 'faculty')

        # Group by Faculty -> Class -> Achievement
        grouped_data = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

        for tp in training_points:
            faculty = tp.faculty.name
            class_name = tp.class_name
            achievement = tp.achievement
            grouped_data[faculty][class_name][achievement].append(tp)

        # Set up PDF response
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="training_points.pdf"'

        p = canvas.Canvas(response, pagesize=letter)
        width, height = letter
        margin = 50
        y_start = height - 50

        p.setFont("Helvetica-Bold", 16)
        p.drawString(margin, y_start, "Training Point Report")
        y = y_start - 30

        p.setFont("Helvetica", 12)

        # Loop over the grouped data to print PDF content
        for faculty, classes in grouped_data.items():
            p.setFont("Helvetica-Bold", 14)
            p.drawString(margin, y, f"Faculty: {faculty}")
            y -= 20

            for class_name, achievements in classes.items():
                p.setFont("Helvetica-Bold", 12)
                p.drawString(margin + 20, y, f"Class: {class_name}")
                y -= 20

                for achievement, records in achievements.items():
                    p.setFont("Helvetica-Bold", 12)
                    p.drawString(margin + 40, y, f"Achievement: {achievement}")
                    y -= 20

                    # Header row for the table
                    p.setFont("Helvetica-Bold", 10)
                    p.drawString(margin + 60, y, "ID")
                    p.drawString(margin + 100, y, "Student Name")
                    p.drawString(margin + 450, y, "Points")
                    y -= 15

                    p.setFont("Helvetica", 10)

                    # Loop through the training points and add them to the PDF
                    for tp in records:
                        if y < 50:  # Start new page if the content goes too low
                            p.showPage()
                            y = height - 50

                        p.drawString(margin + 60, y, str(tp.id))
                        p.drawString(margin + 100, y, tp.user.username)
                        p.drawString(margin + 450, y, str(tp.point))
                        y -= 15

                    y -= 10  # Space after each achievement section

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


class RegisterViewSet(viewsets.ViewSet, generics.UpdateAPIView):
    queryset = Register.objects.all()
    serializer_class = serializers.RegisterSerializer