from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('machine_era', '0002_videoupload'),
    ]

    operations = [
        migrations.CreateModel(
            name='AudioUpload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('audio_file', models.FileField(upload_to='audio_uploads/')),
                ('analysis_result', models.TextField(blank=True, null=True)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
