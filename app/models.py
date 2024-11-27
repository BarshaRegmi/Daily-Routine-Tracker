# app/models.py
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='static/images/photos/', blank=True, null=True)
    profession = models.CharField(max_length=20, choices=[('working', 'Working'), ('student', 'Student')])

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'profession']

    def __str__(self): 
        return self.email 
    
class DayPlan(models.Model):
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateField()
    score = models.FloatField(default=0)
    completed = models.BooleanField(default=False)
    total_compulsary_time = models.TimeField(default='00:00:00')
    total_optional_time = models.TimeField(default='00:00:00')
    completed_compulsary_time = models.TimeField(default='00:00:00')
    completed_optional_time = models.TimeField(default='00:00:00')

    class Meta:
        unique_together = ('user', 'date')  # Ensure unique day-user combinations
        ordering = ['date']

    def __str__(self):
        return f"{self.user.name} : {self.date}"
    

class Task(models.Model):

    DayPlan = models.ForeignKey(DayPlan, on_delete=models.CASCADE, related_name='tasks')

    task = models.CharField(max_length=1000)
    is_completed = models.BooleanField(default=False)
    remarks = models.CharField(max_length=1000, blank=True, null=True)
    description = models.CharField(max_length=1000, blank=True, null=True)
    estimated_time = models.TimeField()

    CATEGORY_CHOICES = [
        ('Compulsory', 'Compulsory'),
        ('Optional', 'Optional'),
    ]
    
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)


    def __str__(self):
        return f"{self.DayPlan.user.name} : {self.DayPlan.date} : {self.category}"
    
class Info(models.Model):
    user = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    streak = models.IntegerField(default = 0)
    photo = models.ImageField(upload_to='static/images/photos/', blank=True, null=True)
    discipline_score = models.FloatField(default = 0)
    freeze_available = models.IntegerField(default = 3)
    last_freeze_used = models.DateField(blank=True, null=True)
    last_active_date = models.DateField(blank=True, null=True)
    total_active_days = models.IntegerField(default = 0)


    def __str__(self):
        return f"{self.user.name}"