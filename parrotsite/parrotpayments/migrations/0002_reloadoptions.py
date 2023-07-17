# Generated by Django 4.2.3 on 2023-07-11 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parrotpayments', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReloadOptions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('num_characters', models.IntegerField()),
                ('price', models.IntegerField(default=0)),
            ],
        ),
    ]