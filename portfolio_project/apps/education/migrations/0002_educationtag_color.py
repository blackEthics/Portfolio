from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='educationtag',
            name='color',
            field=models.CharField(
                choices=[
                    ('red', 'Red'),
                    ('blue', 'Blue'),
                    ('green', 'Green'),
                    ('yellow', 'Yellow'),
                    ('purple', 'Purple'),
                    ('gray', 'Gray'),
                ],
                default='blue',
                max_length=10,
            ),
        ),
    ]
