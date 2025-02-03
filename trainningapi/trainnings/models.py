from ckeditor.fields import RichTextField
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class BaseModel(models.Model):
    active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Faculty(BaseModel):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'khoa'
        verbose_name_plural = 'Khoa'

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
        ('1', 'Điều 1'),
        ('2', 'Điều 2'),
        ('3', 'Điều 3'),
        ('4', 'Điều 4'),
        ('5', 'Điều 5'),
    ]
    title = models.CharField(max_length=255)  # Name activity
    description = RichTextField(null=True)  # Activity description
    image = models.ImageField(upload_to='activities/%Y/%m')
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    max_point = models.IntegerField(default=1, validators=[MaxValueValidator(15), MinValueValidator(1)])
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    criteria = models.CharField(max_length=10, choices=CRITERIA_CHOICES, default='1')  # Choose criteria to add point
    tags = models.ManyToManyField('Tag')  # Add tags for activities

    def __str__(self):
        return self.title


# Student can participate many activities
class Participation(BaseModel):
    ACHIEVEMENT_CHOICES = [
        ('EXCELLENT', 'Excellent'),
        ('GOOD', 'Good'),
        ('AVERAGE', 'Average'),
        ('BELOW AVERAGE', 'Below average'),
        ('WEAK', 'Weak'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, blank=True)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    is_attended = models.BooleanField(default=False)  # Is attend ?
    image = models.ImageField(upload_to='proofs/%Y/%m')  # Proof have attended
    verified = models.BooleanField(default=False)  # Assistant confirm
    achievement = models.CharField(max_length=15, choices=ACHIEVEMENT_CHOICES, null=True, blank=True)
    point = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(15)], null=True,
                                blank=True)

    def __str__(self):
        return f"{self.user} - {self.activity}"


class TrainingPoint(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    class_name = models.CharField(max_length=50, null=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, null=True, blank=True)
    criteria1 = models.IntegerField(default=20, validators=[MinValueValidator(1), MaxValueValidator(50)])
    criteria2 = models.IntegerField(default=25, validators=[MinValueValidator(1), MaxValueValidator(50)])
    criteria3 = models.IntegerField(default=20, validators=[MinValueValidator(1), MaxValueValidator(50)])
    criteria4 = models.IntegerField(default=25, validators=[MinValueValidator(1), MaxValueValidator(50)])
    criteria5 = models.IntegerField(default=10, validators=[MinValueValidator(1), MaxValueValidator(50)])
    point = models.IntegerField(default=100, validators=[MinValueValidator(1), MaxValueValidator(100)])
    achievement = models.CharField(max_length=50, null=True, default='EXCELLENT')

    class Meta:
        verbose_name = 'điểm rèn luyện sinh viên'
        verbose_name_plural = 'điểm rèn luyện sinh viên'

    @property
    def achievement(self):
        if self.point >= 90:
            return 'EXCELLENT'
        elif self.point >= 70:
            return 'GOOD'
        elif self.point >= 50:
            return 'AVERAGE'
        elif self.point >= 40:
            return 'BELOW AVERAGE'
        else:
            return 'WEAK'

    def __str__(self):
        return f"{self.user.username}"


class MissingPointRequest(BaseModel):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='missing_proofs/%Y/%m')
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