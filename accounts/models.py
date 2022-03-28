from django.utils import timezone

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=15)
    region = models.ForeignKey("Region", on_delete=models.SET_NULL, blank=True, null=True, related_name='users')
    address = models.CharField(max_length=255, null=True, blank=True)
    profile = models.CharField(max_length=255)
    place_of_birth = models.CharField(max_length=255, null=True, blank=True)
    skills = models.TextField(max_length=1000, null=True, blank=True)
    hobbies = models.TextField(max_length=1000, null=True, blank=True)
    languages = models.ManyToManyField("Language", blank=True)
    achievements = models.TextField(max_length=1000, null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Region(models.Model):
    name = models.CharField(max_length=255)
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Link(models.Model):
    FACEBOOK = 'FB'
    LINKEDIN = 'LI'
    GITHUB = 'GH'

    LINK_CHOICES = [
        (FACEBOOK, 'Facebook'),
        (LINKEDIN, 'LinkedIn'),
        (GITHUB, 'GitHub'),
    ]

    type = models.CharField(choices=LINK_CHOICES, default=FACEBOOK, max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='links')
    link = models.URLField()
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.type


class Language(models.Model):
    title = models.CharField(max_length=255)
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class EducationAndEmploymentHistory(models.Model):
    EDUCATION = 'ED'
    EMPLOYMENT = 'EM'

    TYPE_CHOICES = [
        (EDUCATION, 'Education'),
        (EMPLOYMENT, 'Employment'),
    ]

    type = models.CharField(choices=TYPE_CHOICES, default=EDUCATION, max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='history')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    starting_date = models.DateTimeField(auto_now_add=True)
    ending_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
