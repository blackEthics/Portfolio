from django.db import models


class EducationTag(models.Model):
    name = models.CharField(max_length=80, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Education(models.Model):
    degree = models.CharField(max_length=200)
    school = models.CharField(max_length=200)
    start_year = models.CharField(max_length=10)
    end_year = models.CharField(max_length=10)
    grade = models.CharField(max_length=50, blank=True)
    icon_emoji = models.CharField(max_length=10, default='🎓')
    tags = models.ManyToManyField(EducationTag, blank=True, related_name='educations')
    order = models.PositiveIntegerField(default=0, db_index=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Education'
        verbose_name_plural = 'Education'

    def __str__(self):
        return f'{self.degree} — {self.school}'

    @property
    def period(self):
        return f'{self.start_year} – {self.end_year}'
