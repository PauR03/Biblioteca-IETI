# Generated by Django 5.0.4 on 2024-05-03 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biblioteca', '0007_remove_producte_idimatge_producte_imatge_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='telefon',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]