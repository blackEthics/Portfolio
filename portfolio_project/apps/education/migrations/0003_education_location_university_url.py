from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0002_educationtag_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='education',
            name='location',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='education',
            name='university_url',
            field=models.URLField(blank=True),
        ),
    ]
