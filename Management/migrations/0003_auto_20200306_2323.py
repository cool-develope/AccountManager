# -*- coding: utf-8 -*-
# Generated by Django 1.11.21 on 2020-03-06 15:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Management', '0002_auto_20200306_2247'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('comment', models.TextField(blank=True)),
                ('host', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterModelOptions(
            name='rebalance',
            options={'ordering': ('-request_date',)},
        ),
        migrations.AddField(
            model_name='account',
            name='client',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='accounts', to='Management.Client'),
            preserve_default=False,
        ),
    ]