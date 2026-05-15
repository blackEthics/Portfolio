import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='VolunteeringOrganization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('location', models.CharField(blank=True, max_length=150)),
                ('logo_initials', models.CharField(blank=True, max_length=6)),
                ('logo_image', models.ImageField(blank=True, null=True, upload_to='org_logos/')),
                ('total_duration', models.CharField(blank=True, max_length=100)),
                ('order', models.PositiveIntegerField(db_index=True, default=0)),
            ],
            options={
                'verbose_name': 'Volunteering Organization',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='VolunteeringRole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('start_date', models.CharField(max_length=50)),
                ('end_date', models.CharField(blank=True, max_length=50)),
                ('is_current', models.BooleanField(default=False)),
                ('description', models.TextField(blank=True)),
                ('achievements', models.TextField(blank=True)),
                ('order', models.PositiveIntegerField(db_index=True, default=0)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='roles', to='volunteering.volunteeringorganization')),
            ],
            options={
                'verbose_name': 'Volunteering Role',
                'ordering': ['order'],
            },
        ),
    ]
