# Generated by Django 4.1.7 on 2023-05-15 08:12

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_product_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
