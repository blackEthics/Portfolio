from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('experience', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='experiencetag',
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
                default='green',
                max_length=10,
            ),
        ),
    ]
