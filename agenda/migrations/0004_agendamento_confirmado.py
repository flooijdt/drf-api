# Generated by Django 4.0.3 on 2022-04-04 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0003_agendamento_prestador'),
    ]

    operations = [
        migrations.AddField(
            model_name='agendamento',
            name='confirmado',
            field=models.BooleanField(default=False),
        ),
    ]
