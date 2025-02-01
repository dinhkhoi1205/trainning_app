
from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField
from cloudinary.models import CloudinaryField


class BaseModel(models.Model):
    active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Faculty(BaseModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    avatar = CloudinaryField(null=True)

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
    tags = models.ManyToManyField('Tag')  # Add tags for activities

    def __str__(self):
        return self.title


# Student can participate many activities
class Participation(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, blank=True)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add=True)
    is_attended = models.BooleanField(default=False)  # Is attend ?
    image = models.ImageField(upload_to='proofs/%Y/%m')  # Proof have attended
    verified = models.BooleanField(default=False)  # Assistant confirm
    class_name = models.CharField(max_length=50, null=True)

    def __str__(self):
        return f"{self.user} - {self.activity}"


class TrainingPoint(BaseModel):
    ACHIEVEMENT_CHOICES = [
        ('EXCELLENT', 'Excellent'),
        ('GOOD', 'Good'),
        ('AVERAGE', 'Average'),
        ('BELOW AVERAGE', 'Below average'),
        ('WEAK', 'Weak'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    criteria = models.CharField(max_length=1, choices=Activity.CRITERIA_CHOICES)
    point = models.IntegerField(default=0)
    achievement = models.CharField(max_length=15, choices=ACHIEVEMENT_CHOICES, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.activity.title} - {self.criteria}"


class MissingPointRequest(BaseModel):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    proof_image = models.ImageField(upload_to='missing_proofs/%Y/%m')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')

    def __str__(self):
        return f"{self.user.username} - {self.activity.title}"


class Tag(BaseModel):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Interaction(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class Comment(Interaction):
    content = models.TextField()


class Like(Interaction):
    class Meta:
        unique_together = ('user', 'activity')
