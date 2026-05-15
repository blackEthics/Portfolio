from django.db import models
from django.utils.text import slugify


class WriteupTag(models.Model):
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


class Writeup(models.Model):
    CATEGORY_CHOICES = [
        ('cve', 'CVE Research'),
        ('ctf', 'CTF Writeup'),
        ('bug_bounty', 'Bug Bounty'),
        ('red_team', 'Red Teaming'),
        ('tools', 'Tools & Techniques'),
        ('pentest', 'Penetration Testing'),
    ]
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    ]

    thumb_label = models.CharField(
        max_length=40,
        help_text='Thumbnail text — use | for a line break (e.g. "CVE-2026|Linux")',
    )
    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True, blank=True)
    excerpt = models.TextField()
    content = models.TextField(blank=True, help_text='Full writeup body (Markdown supported)')
    tags = models.ManyToManyField(WriteupTag, blank=True, related_name='writeups')
    thumbnail = models.ImageField(upload_to='writeups/', blank=True, null=True)
    published_at = models.DateField()
    read_time_min = models.PositiveIntegerField(default=5)
    read_time_max = models.PositiveIntegerField(default=10)
    is_featured = models.BooleanField(default=False, db_index=True)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='ctf')
    difficulty_level = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='intermediate')

    class Meta:
        ordering = ['-published_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def read_time_display(self):
        return f'{self.read_time_min}–{self.read_time_max} min read'

    def thumb_lines(self):
        return self.thumb_label.split('|')

    @property
    def difficulty_color(self):
        return {
            'beginner': 'green',
            'intermediate': 'blue',
            'advanced': 'yellow',
            'expert': 'red',
        }.get(self.difficulty_level, 'gray')

    @property
    def category_display(self):
        return dict(self.CATEGORY_CHOICES).get(self.category, self.category)
