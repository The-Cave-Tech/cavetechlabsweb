"""
Models for the Cave Tech Labs website.
"""
from django.db import models
from django.utils.text import slugify


class Person(models.Model):
    """Model representing a member of the Cave Tech Labs."""
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=200, blank=True, help_text="e.g., Founder, Lead Instructor")
    bio = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    image = models.ImageField(upload_to='people/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'People'

    def __str__(self):
        return self.name


class Project(models.Model):
    """Model representing a project created at or by members of Cave Tech Labs."""
    CATEGORY_CHOICES = [
        ('3d_printing', '3D Printing'),
        ('woodworking', 'Woodworking'),
        ('metalworking', 'Metalworking'),
        ('electronics', 'Electronics'),
        ('software', 'Software'),
        ('art', 'Art & Design'),
        ('robotics', 'Robotics'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    creator = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True, blank=True, related_name='projects')
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Auto-generate slug if not provided."""
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
