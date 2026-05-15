from django.db import models
from django.utils.text import slugify


class ProjectTag(models.Model):
    COLOR_CHOICES = [
        ('red', 'Red'),
        ('blue', 'Blue'),
        ('green', 'Green'),
        ('yellow', 'Yellow'),
        ('purple', 'Purple'),
        ('gray', 'Gray'),
    ]
    name = models.CharField(max_length=80, unique=True)
    color = models.CharField(max_length=10, choices=COLOR_CHOICES, default='gray')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    thumb_label = models.CharField(
        max_length=40,
        help_text='Thumbnail text — use | for a line break (e.g. "HTB|Fortress")',
    )
    excerpt = models.TextField()
    description = models.TextField(blank=True)
    tags = models.ManyToManyField(ProjectTag, blank=True, related_name='projects')
    project_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    thumbnail = models.ImageField(upload_to='projects/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def thumb_lines(self):
        return self.thumb_label.split('|')
