from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('volunteering', '0002_alter_volunteeringorganization_logo_initials_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='volunteeringorganization',
            name='category',
            field=models.CharField(
                choices=[
                    ('tech', 'Tech & Innovation'),
                    ('social', 'Social Impact'),
                    ('academic', 'Academic'),
                    ('leadership', 'Club Leadership'),
                    ('other', 'Other'),
                ],
                default='other',
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name='volunteeringorganization',
            name='featured',
            field=models.BooleanField(
                default=False,
                help_text='Show this org on the homepage volunteering preview.',
            ),
        ),
    ]
