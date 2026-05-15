from django.db import models


class SkillCategory(models.Model):
    label = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0, db_index=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Skill Category'
        verbose_name_plural = 'Skill Categories'

    def __str__(self):
        return self.label


class Skill(models.Model):
    category = models.ForeignKey(
        SkillCategory, on_delete=models.CASCADE, related_name='skills'
    )
    name = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return f'{self.category.label}: {self.name}'
