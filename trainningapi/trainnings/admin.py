from django.contrib import admin
from django.contrib.auth.models import Group
from django.db.models import Count, Avg, Sum
from django.template.response import TemplateResponse
from django.urls import path
from django.utils.safestring import mark_safe

from trainnings.models import (Category, Activity, Participation, User, Comment, Faculty,
                               TrainingPoint, MissingPointRequest, Tag)


class MyAppAdmin(admin.AdminSite):
    site_header = 'Training Point Management'

    def get_urls(self):
        return [path('training-stats/', self.stats)] + super().get_urls()

    def stats(self, request):
        # Stats training points as faculty, class, achievement
        stats_by_faculty = (
            Participation.objects.values('faculty__name')
            .annotate(
                total_students=Count('id'),
            )
            .order_by('faculty')
        )
        stats_by_class = (
            TrainingPoint.objects.values('class_name')
            .annotate(
                total_students=Count('id'),
            )
            .order_by('class_name')
        )

        stats_by_achievement = {
            "EXCELLENT": TrainingPoint.objects.filter(point__gte=90).count(),
            "GOOD": TrainingPoint.objects.filter(point__gte=70, point__lt=90).count(),
            "AVERAGE": TrainingPoint.objects.filter(point__gte=50, point__lt=70).count(),
            "BELOW_AVERAGE": TrainingPoint.objects.filter(point__gte=30, point__lt=50).count(),
            "WEAK": TrainingPoint.objects.filter(point__lt=30).count(),
        }

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


class ActivityAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'category', 'description',
                    'max_point', 'start_date', 'end_date', 'active']
    search_fields = ['title']
    list_filter = ['category', 'start_date', 'end_date', 'active']
    ordering = ['start_date']
    readonly_fields = ['display_image']

    def display_image(self, activities):
        return mark_safe(f"<img src='/static/{activities.image.name}' width = '120' />")


class ParticipationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'faculty', 'activity', 'point',
                    'achievement', 'is_attended', 'verified', 'created_date']
    search_fields = ['user', ]
    list_filter = ['is_attended', 'verified', 'created_date']
    ordering = ['created_date']
    readonly_fields = ['display_proof']

    def display_proof(self, proofs):
        return mark_safe(f"<img src='/static/{proofs.image.name}' width = '120' />")

    def activity_max_point(self, participation):
        return participation.activity.max_point


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'email', 'is_staff']
    list_filter = ['is_staff']


class TrainingPointAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'point', 'created_date', 'achievement']
    search_fields = ['user__username']
    list_filter = ['created_date', 'user', 'user__username']
    ordering = ['created_date']
    readonly_fields = ['achievement']

    def achievement(self, obj):
        return obj.achievement


class MissingPointRequestAdmin(admin.ModelAdmin):
    list_display = ['user', 'activity', 'status', 'created_date']
    search_fields = ['user__username', 'activity__title']
    list_filter = ['status', 'created_date']
    ordering = ['created_date']
    readonly_fields = ['display_proof']

    def display_proof(self, missing_proofs):
        return mark_safe(f"<img src='/static/{missing_proofs.image.name}' width = '120' />")


class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_date']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'content', 'created_date']


# Register your models here.
admin_site = MyAppAdmin(name='Training App')
admin_site.index_template = ['admin/custom-admin-index.html']
admin_site.register(Category, CategoryAdmin)
admin_site.register(Activity, ActivityAdmin)
admin_site.register(Tag, TagAdmin)
admin_site.register(Comment, CommentAdmin)
admin_site.register(User, UserAdmin)
admin_site.register(Faculty, FacultyAdmin)
admin_site.register(TrainingPoint, TrainingPointAdmin)
admin_site.register(MissingPointRequest, MissingPointRequestAdmin)
admin_site.register(Group)
admin_site.register(Participation, ParticipationAdmin)