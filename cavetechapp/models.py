"""
Models for the Cave Tech Labs website.
"""
from django.db import models
from django.utils.text import slugify


class SiteSettings(models.Model):
    """Model for storing site-wide settings like About Us, Contact Info, etc."""
    about_title = models.CharField(max_length=200, default="About The Cave Tech")
    about_content = models.TextField(blank=True, help_text="Main about us content")
    history = models.TextField(blank=True, help_text="History section content")
    address = models.TextField(blank=True, help_text="Physical address")
    email = models.EmailField(blank=True, help_text="Contact email address")
    instagram = models.URLField(blank=True, help_text="Instagram profile URL")
    phone = models.CharField(max_length=20, blank=True, help_text="Contact phone number")
    image = models.ImageField(upload_to='about/', blank=True, null=True, help_text="Hero image for About Us page")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return "Site Settings"

    def save(self, *args, **kwargs):
        """Ensure only one SiteSettings instance exists."""
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """Prevent deletion of SiteSettings."""
        pass

    @classmethod
    def get_settings(cls):
        """Get or create the singleton SiteSettings instance."""
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class Category(models.Model):
    """Model representing a project category."""
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Auto-generate slug if not provided."""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


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
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='projects')
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
