# Generated by Django 4.2.1 on 2024-05-26 12:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rentals', '0003_remove_userprofile_is_buyer'),
    ]

    operations = [
        migrations.CreateModel(
            name='PropertyPhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='property_photos/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='rentals.property')),
            ],
        ),
    ]
