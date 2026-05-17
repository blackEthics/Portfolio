from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='siteprofile',
            name='twitter_url',
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name='siteprofile',
            name='facebook_url',
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name='siteprofile',
            name='whatsapp_url',
            field=models.URLField(blank=True, help_text='Full wa.me link, e.g. https://wa.me/8801XXXXXXXXX'),
        ),
    ]
