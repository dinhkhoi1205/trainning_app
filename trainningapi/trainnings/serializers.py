from django.template.context_processors import request

from trainnings.models import (Category, Activity, Participation,
                               Tag, Comment, User, TrainingPoint, MissingPointRequest, Register,StatusRegister)
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class BaseSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, activity):
        if activity.image:
            if activity.image.name.startswith("http"):
                return activity.image.name
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri('/static/%s' % activity.image.name)
            return None


class UserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        data = validated_data.copy()
        u = User(**data)
        u.set_password(u.password)
        u.save()
        return u

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['avatar'] = instance.avatar.url if instance.avatar else ''
        return data

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'avatar']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class ActivitySerializer(BaseSerializer):
    category = CategorySerializer()
    tags = TagSerializer(many=True)

    class Meta:
        model = Activity
        fields = ['id', 'title', 'description', 'max_point', 'start_date', 'end_date',
                  'active', 'category', 'image', 'tags']


class ParticipationSerializer(BaseSerializer):
    activity = ActivitySerializer()
    user = UserSerializer()

    class Meta:
        model = Participation
        fields = ['id', 'user', 'image',
                  'activity', 'is_attended', 'verified', 'point']


class ActivityDetailsSerializer(ParticipationSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = ActivitySerializer.Meta.model
        fields = ActivitySerializer.Meta.fields + ['description', 'tags']


class TrainingPointSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = TrainingPoint
        fields = '__all__'


class MissingPointRequestSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    activity = ActivitySerializer()
    proof_image_url = serializers.SerializerMethodField()

    def get_proof_image_url(self, obj):
        if obj.image:
            return obj.image.url
        return None

    class Meta:
        model = MissingPointRequest
        fields = ['id', 'user', 'activity', 'proof_image_url', 'status']


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Comment
        fields = '__all__'


class RegisterSerializer(serializers.ModelSerializer):
    student = TrainingPointSerializer()
    activity = ActivityDetailsSerializer()

    class Meta:
        model = Register
        fields = ['activity', 'student', 'status']


class RegisterCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Register
        fields = ['status']


class RegisterCurrentSerializer(serializers.ModelSerializer):
    activity = ParticipationSerializer()

    class Meta:
        model = Register
        fields = ['activity']
