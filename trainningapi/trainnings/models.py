from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField
from cloudinary.models import CloudinaryField


class User(AbstractUser):
    avatar = CloudinaryField(null=True)


class BaseModel(models.Model):
    active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# Save active category
class Category(BaseModel):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


# Activity detail in category
class Activity(BaseModel):
    CRITERIA_CHOICES = [
        ('1', 'Criteria 1'),
        ('2', 'Criteria 2'),
        ('3', 'Criteria 3'),
        ('4', 'Criteria 4'),
        ('5', 'Criteria 5'),
    ]
    title = models.CharField(max_length=255)  # Name activity
    description = RichTextField(null=True)  # Activity description
    image = models.ImageField(upload_to='activities/%Y/%m')
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    max_point = models.IntegerField(default=0)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    criteria = models.CharField(max_length=1, choices=CRITERIA_CHOICES, default='1')  # Choose criteria to add point
    tags = models.ManyToManyField('Tag') #Add tags for activities

    def __str__(self):
        return self.title


# Student can participate many activities
class Participation(BaseModel):
    FACULTY_CHOICES = [
        ('TE', 'Technology'),
        ('LA', 'Law'),
        ('EL', 'English language'),
        ('TOUR', 'Tourist'),
        ('HOM', 'Hotel management'),
    ]

    ACHIEVEMENT_CHOICES = [
        ('EXCELLENT', 'Excellent'),
        ('GOOD', 'Good'),
        ('AVERAGE', 'Average'),
        ('BELOW AVERAGE', 'Below average'),
        ('WEAK', 'Weak'),
    ]
    user = models.CharField(max_length=255)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    is_attended = models.BooleanField(default=False)  # Is attend ?
    image = models.ImageField(upload_to='proofs/%Y/%m')  # Proof have attended
    verified = models.BooleanField(default=False)  # Assistant confirm
    class_name = models.CharField(max_length=50, null=True)
    faculty = models.CharField(max_length=10, choices=FACULTY_CHOICES, null=True, blank=True)
    achievement = models.CharField(max_length=15, choices=ACHIEVEMENT_CHOICES, null=True, blank=True)
    point = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user} - {self.activity} - {self.faculty}"


class Tag(BaseModel):
    name = models.CharField(max_length=50, unique=True)


class Interaction(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    participation = models.ForeignKey(Participation, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class Comment(Interaction):
    content = models.CharField(max_length=255, null=False)


class Like(Interaction):
    class Meta:
        unique_together = ('user', 'participation')