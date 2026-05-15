from django.db import models


class ExperienceTag(models.Model):
    name = models.CharField(max_length=80, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Experience(models.Model):
    EMPLOYMENT_CHOICES = [
        ('full_time', 'Full-time'),
        ('part_time', 'Part-time'),
        ('internship', 'Internship'),
        ('contract', 'Contract'),
        ('freelance', 'Freelance'),
    ]
    WORK_MODE_CHOICES = [
        ('on_site', 'On-site'),
        ('remote', 'Remote'),
        ('hybrid', 'Hybrid'),
    ]
    DOT_CHOICES = [('red', 'Red'), ('green', 'Green')]

    title = models.CharField(max_length=150)
    company = models.CharField(max_length=150)
    employment_type = models.CharField(
        max_length=20, choices=EMPLOYMENT_CHOICES, default='full_time'
    )
    location = models.CharField(max_length=100)
    work_mode = models.CharField(
        max_length=20, choices=WORK_MODE_CHOICES, default='on_site'
    )
    start_date = models.CharField(max_length=20, help_text='e.g. 2024 or Mar 2024')
    end_date = models.CharField(
        max_length=20, blank=True, help_text='Leave blank if current'
    )
    is_current = models.BooleanField(default=False)
    description = models.TextField()
    tags = models.ManyToManyField(ExperienceTag, blank=True, related_name='experiences')
    dot_color = models.CharField(max_length=10, choices=DOT_CHOICES, default='red')
    order = models.PositiveIntegerField(default=0, db_index=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Experience'

    def __str__(self):
        return f'{self.title} at {self.company}'

    @property
    def period(self):
        end = 'Present' if self.is_current else self.end_date
        return f'{self.start_date} – {end}'

    def get_employment_display_label(self):
        return dict(self.EMPLOYMENT_CHOICES).get(self.employment_type, self.employment_type)

    def get_work_mode_display_label(self):
        return dict(self.WORK_MODE_CHOICES).get(self.work_mode, self.work_mode)


class Achievement(models.Model):
    experience = models.ForeignKey(
        Experience, on_delete=models.CASCADE, related_name='achievements'
    )
    text = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.text[:60]
