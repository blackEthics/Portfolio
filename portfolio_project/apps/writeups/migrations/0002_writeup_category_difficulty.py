from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('writeups', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='writeup',
            name='category',
            field=models.CharField(
                choices=[
                    ('cve', 'CVE Research'),
                    ('ctf', 'CTF Writeup'),
                    ('bug_bounty', 'Bug Bounty'),
                    ('red_team', 'Red Teaming'),
                    ('tools', 'Tools & Techniques'),
                    ('pentest', 'Penetration Testing'),
                ],
                default='ctf',
                max_length=30,
            ),
        ),
        migrations.AddField(
            model_name='writeup',
            name='difficulty_level',
            field=models.CharField(
                choices=[
                    ('beginner', 'Beginner'),
                    ('intermediate', 'Intermediate'),
                    ('advanced', 'Advanced'),
                    ('expert', 'Expert'),
                ],
                default='intermediate',
                max_length=20,
            ),
        ),
    ]
