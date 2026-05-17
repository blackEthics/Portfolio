from django.db import models


class VolunteeringOrganization(models.Model):
    CATEGORY_CHOICES = [
        ('tech', 'Tech & Innovation'),
        ('social', 'Social Impact'),
        ('academic', 'Academic'),
        ('leadership', 'Club Leadership'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=150)
    location = models.CharField(max_length=150, blank=True)
    logo_initials = models.CharField(
        max_length=6, blank=True,
        help_text='Short initials shown when no logo image is set, e.g. "IEEE"',
    )
    logo_image = models.ImageField(upload_to='org_logos/', blank=True, null=True)
    total_duration = models.CharField(
        max_length=100, blank=True,
        help_text='e.g. "Jan 2023 – Present · 2 yrs"',
    )
    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, default='other',
    )
    featured = models.BooleanField(
        default=False,
        help_text='Show this org on the homepage volunteering preview.',
    )
    order = models.PositiveIntegerField(default=0, db_index=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Volunteering Organization'

    def __str__(self):
        return self.name


class VolunteeringRole(models.Model):
    organization = models.ForeignKey(
        VolunteeringOrganization,
        on_delete=models.CASCADE,
        related_name='roles',
    )
    title = models.CharField(max_length=150)
    start_date = models.CharField(max_length=50, help_text='e.g. "Jan 2025"')
    end_date = models.CharField(
        max_length=50, blank=True,
        help_text='Leave blank if current role',
    )
    is_current = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    achievements = models.TextField(
        blank=True,
        help_text='One achievement per line',
    )
    order = models.PositiveIntegerField(default=0, db_index=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Volunteering Role'

    def __str__(self):
        return f'{self.title} at {self.organization.name}'

    @property
    def period(self):
        end = 'Present' if (self.is_current or not self.end_date) else self.end_date
        return f'{self.start_date} – {end}'

    def get_achievements_list(self):
        return [a.strip() for a in self.achievements.splitlines() if a.strip()]
