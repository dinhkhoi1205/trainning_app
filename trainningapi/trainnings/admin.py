from django.contrib import admin
from django.contrib.auth.models import Group
from django.db.models import Count, Avg, Sum
from django.utils.safestring import mark_safe
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from trainnings.models import Category, Activity, Participation, Tag, User, Comment
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
                total_points=Sum('point'),
            )
            .order_by('faculty')
        )
        stats_by_class = (
            Participation.objects.values('class_name')
            .annotate(
                total_students=Count('id'),
                total_points=Sum('point'),
            )
            .order_by('class_name')
        )

        stats_by_achievement = (
            Participation.objects.values('achievement')
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


class ActivityForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = Activity
        fields = '__all__'


class ActivityAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'category', 'max_point', 'start_date', 'end_date', 'active']
    search_fields = ['title']
    list_filter = ['category', 'start_date', 'end_date', 'active']
    ordering = ['start_date']
    readonly_fields = ['display_image']
    forms = ActivityForm

    def display_image(self, activities):
        return mark_safe(f"<img src='/static/{activities.image.name}' width = '120' />")


class ParticipationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'faculty','class_name', 'activity', 'point',
                    'achievement','is_attended', 'verified', 'created_date']
    search_fields = ['user__username', 'faculty', 'class_name']
    list_filter = ['is_attended', 'verified', 'created_date']
    ordering = ['created_date']
    readonly_fields = ['display_proof']

    def display_proof(self, proofs):
        return mark_safe(f"<img src='/static/{proofs.image.name}' width = '120' />")

    def activity_max_point(self, participation):
        return participation.activity.max_point

# Register your models here.
admin_site = MyAppAdmin(name='Training App')
admin_site.register(Category, CategoryAdmin)
admin_site.register(Activity, ActivityAdmin)
admin_site.register(Tag)
admin_site.register(Comment)
admin_site.register(User)
admin_site.register(Group)
admin_site.register(Participation, ParticipationAdmin)
