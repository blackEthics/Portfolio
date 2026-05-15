from django.db import models


class Certification(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('in_progress', 'In Progress'),
    ]

    name = models.CharField(max_length=200)
    short_name = models.CharField(max_length=80, help_text='Short label for sidebar tab')
    category = models.CharField(max_length=100)
    issuer = models.CharField(max_length=100)
    issue_date = models.CharField(max_length=50, help_text='e.g. 2024 or Jun 2025')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    description = models.TextField()
    cert_image = models.ImageField(upload_to='certifications/', blank=True, null=True)
    credential_url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0, db_index=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Certification'

    def __str__(self):
        return self.name

    @property
    def status_color(self):
        colors = {
            'active': '#3fb950',
            'expired': '#f85149',
            'in_progress': '#ffa657',
        }
        return colors.get(self.status, '#3fb950')
