# Generated by Django 5.1.2 on 2024-10-27 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sole", "0004_alter_game_buyer"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="game",
            name="buyer",
        ),
        migrations.AddField(
            model_name="game",
            name="buyer",
            field=models.ManyToManyField(related_name="game", to="sole.buyer"),
        ),
    ]
