import json
from django.db import models


class SiteProfile(models.Model):
    name = models.CharField(max_length=100)
    hero_label = models.CharField(max_length=100, default="Hi, I'm a")
    title_roles = models.TextField(
        help_text='One role per line — used for the typewriter animation',
        default='Vulnerability Assessment\nPenetration Tester\nCybersecurity Engineer',
    )
    bio = models.TextField()
    profile_photo = models.ImageField(upload_to='profile/', blank=True, null=True)
    profile_initials = models.CharField(max_length=4, default='YN')
    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    tryhackme_url = models.URLField(blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    location = models.CharField(max_length=100, blank=True)
    response_note = models.TextField(
        blank=True,
        default="I typically respond to all inquiries within 24 hours. For urgent security matters, please call directly.",
    )
    footer_tagline = models.CharField(max_length=200, default='Stay curious. Stay ethical.')
    footer_location = models.CharField(max_length=50, default='Dhaka')

    class Meta:
        verbose_name = 'Site Profile'
        verbose_name_plural = 'Site Profile'

    def __str__(self):
        return self.name

    def get_roles(self):
        return [r.strip() for r in self.title_roles.splitlines() if r.strip()]

    def get_roles_json(self):
        return json.dumps(self.get_roles())


class ContactMessage(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Message'

    def __str__(self):
        return f'{self.first_name} {self.last_name} — {self.subject}'
