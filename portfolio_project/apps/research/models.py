from django.db import models


class ResearchTag(models.Model):
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


class ResearchPaper(models.Model):
    title = models.CharField(max_length=400)
    authors = models.CharField(
        max_length=500,
        help_text='Comma-separated list of authors',
    )
    abstract = models.TextField(help_text='Full abstract of the paper')
    short_description = models.TextField(
        max_length=300,
        help_text='Brief description shown on the card (max 300 chars)',
    )
    venue = models.CharField(
        max_length=200,
        help_text='Journal or conference name (e.g. "IEEE Access", "NDSS 2024")',
    )
    published_at = models.DateField()
    publication_url = models.URLField(
        blank=True,
        help_text='Link to the paper on the publisher site (IEEE, ACM, etc.)',
    )
    certificate_image = models.ImageField(
        upload_to='research/certificates/',
        blank=True,
        null=True,
        help_text='Upload the publication certificate image',
    )
    tags = models.ManyToManyField(ResearchTag, blank=True, related_name='papers')
    is_featured = models.BooleanField(default=True, db_index=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', '-published_at']

    def __str__(self):
        return self.title

    def get_authors_list(self):
        return [a.strip() for a in self.authors.split(',') if a.strip()]
