from django.contrib import admin
from django.contrib.auth.models import Group
from django.db.models import Count, Avg, Sum
from django.utils.safestring import mark_safe
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from trainnings.models import (Category, Activity, Participation, Tag, User, Comment, Faculty,
                               TrainingPoint, MissingPointRequest)
from django.urls import path
from django.template.response import TemplateResponse


class MyAppAdmin(admin.AdminSite):
    site_header = 'Training Point Management'
    site_title = 'Training Point Admin'

    def get_urls(self):
        return [path('training-stats/', self.stats)] + super().get_urls()

    def stats(self, request):
        # Stats training points as faculty, class, achievement
        stats_by_faculty = (
            Participation.objects.values('faculty')
            .annotate(
                total_students=Count('id'),
            )
            .order_by('faculty')
        )
        stats_by_class = (
            Participation.objects.values('class_name')
            .annotate(
                total_students=Count('id'),
            )
            .order_by('class_name')
        )

        stats_by_achievement = (
            TrainingPoint.objects.values('achievement')
            .annotate(
                total_students=Count('id'),
                average_points=Avg('point'),
            )
            .order_by('achievement')
        )

        return TemplateResponse(request, 'admin/stats.html', {
            'stats_by_faculty': stats_by_faculty,
            'stats_by_class': stats_by_class,
            'stats_by_achievement': stats_by_achievement,
        })


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'active', 'created_date', 'updated_date']
    search_fields = ['name']
    list_filter = ['active', 'created_date']
    ordering = ['name']


class FacultyAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_date', 'updated_date']
    search_fields = ['name']
    ordering = ['name']


class ActivityForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = Activity
        fields = '__all__'


class ActivityAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'category', 'description',
                    'max_point', 'start_date', 'end_date', 'active']
    search_fields = ['title']
    list_filter = ['category', 'start_date', 'end_date', 'active']
    ordering = ['start_date']
    readonly_fields = ['display_image']
    form = ActivityForm

    def display_image(self, activities):
        return mark_safe(f"<img src='/static/{activities.image.name}' width = '120' />")


class ParticipationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'faculty', 'class_name', 'activity',
                    'is_attended', 'verified', 'registered_at', 'created_date']
    search_fields = ['user__username', 'class_name']
    list_filter = ['is_attended', 'verified', 'created_date']
    ordering = ['created_date']
    readonly_fields = ['display_proof']

    def display_proof(self, proofs):
        return mark_safe(f"<img src='/static/{proofs.image.name}' width = '120' />")


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_staff']
    list_filter = ['is_staff']


class TrainingPointAdmin(admin.ModelAdmin):
    list_display = ['user', 'activity', 'criteria', 'point', 'display_activity_points', 'created_date']
    search_fields = ['user__username', 'activity__title']
    list_filter = ['criteria', 'created_date']
    ordering = ['created_date']

    def display_activity_points(self, obj):
        return obj.activity.max_point


class MissingPointRequestAdmin(admin.ModelAdmin):
    list_display = ['user', 'activity', 'status', 'created_date']
    search_fields = ['user__username', 'activity__title']
    list_filter = ['status', 'created_date']
    ordering = ['created_date']
    readonly_fields = ['display_proof']

    def display_proof(self, missing_proofs):
        return mark_safe(f"<img src='/static/{missing_proofs.image.name}' width = '120' />")


# Register your models here.
admin_site = MyAppAdmin(name='Training App')
admin_site.register(Category, CategoryAdmin)
admin_site.register(Activity, ActivityAdmin)
admin_site.register(Tag)
admin_site.register(Comment)
admin_site.register(User, UserAdmin)
admin_site.register(Faculty, FacultyAdmin)
admin_site.register(TrainingPoint, TrainingPointAdmin)
admin_site.register(MissingPointRequest, MissingPointRequestAdmin)
admin_site.register(Group)
admin_site.register(Participation, ParticipationAdmin)
