# Generated by Django 3.2.3 on 2025-04-10 09:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pos', '0002_alter_sale_server'),
    ]

    operations = [
        migrations.AlterField(
            model_name='saleitem',
            name='sale',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='pos.sale'),
        ),
    ]
