from django.db import models


class ServiceTag(models.Model):
    COLOR_CHOICES = [
        ('red', 'Red'),
        ('blue', 'Blue'),
        ('green', 'Green'),
        ('yellow', 'Yellow'),
        ('purple', 'Purple'),
        ('gray', 'Gray'),
    ]
    name = models.CharField(max_length=80, unique=True)
    color = models.CharField(max_length=10, choices=COLOR_CHOICES, default='blue')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Service(models.Model):
    icon = models.CharField(max_length=20, help_text='Emoji or short HTML string')
    title = models.CharField(max_length=100)
    description = models.TextField()
    tags = models.ManyToManyField(ServiceTag, blank=True, related_name='services')
    order = models.PositiveIntegerField(default=0, db_index=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title
