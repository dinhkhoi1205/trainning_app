from django.template.context_processors import request

from trainnings.models import Category, Activity, Participation, Tag, Comment, User
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class BaseSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(source='image')

    def get_image(self, activity):

        if activity.image:
            if activity.image.name.startswith("http"):
                return activity.image.name

            request = self.context.get('request')
            if request:
                return request.build_absolute_uri('/static/%s' % activity.image.name)

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class ActivitySerializer(BaseSerializer):
    category = CategorySerializer()
    tags = TagSerializer(many=True)

    class Meta:
        model = Activity
        fields = ['id', 'title', 'description', 'max_point', 'start_date', 'end_date', 'active', 'category', 'image', 'tags']

class ParticipationSerializer(BaseSerializer):
    activity = ActivitySerializer()

    class Meta:
        model = Participation
        fields = ['id', 'user', 'image', 'class_name', 'faculty', 'activity']


class ParticipationDetailsSerializer(ParticipationSerializer):
    tags = TagSerializer(many=True, source='activity.tags')

    class Meta:
        model = ParticipationSerializer.Meta.model
        fields = ParticipationSerializer.Meta.fields + ['tags']


class UserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        data = validated_data.copy()
        u = User(**data)
        u.set_password(u.password)
        u.save()

        return u

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['avatar'] = instance.avatar.url if instance.avatar.url else ''
        return data


    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'avatar']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Comment
        fields = '__all__'