# Generated by Django 4.0.3 on 2022-04-04 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("agenda", "0004_agendamento_confirmado"),
    ]

    operations = [
        migrations.AddField(
            model_name="agendamento",
            name="executado",
            field=models.BooleanField(default=False),
        ),
    ]
