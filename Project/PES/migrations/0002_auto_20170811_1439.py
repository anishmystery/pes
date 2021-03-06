# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-08-11 09:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('PES', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdditionalSkill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Threshold', models.IntegerField()),
                ('IsCompleted', models.BooleanField()),
                ('Employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PES.Employee')),
                ('Skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PES.Skill')),
            ],
        ),
        migrations.CreateModel(
            name='AdditionalSkillReview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Review', models.IntegerField()),
                ('ReviewedOn', models.DateField()),
                ('AdditionalSkill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PES.AdditionalSkill')),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeAuthority',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('IsActive', models.BooleanField()),
                ('ActiveFrom', models.DateField()),
                ('ActiveTo', models.DateField()),
                ('Authority', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='AuthorityId', to='PES.Employee')),
                ('Employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='EmployeeId', to='PES.Employee')),
            ],
        ),
        migrations.CreateModel(
            name='SkillDesignation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Threshold', models.IntegerField()),
                ('Department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PES.Department')),
                ('Designation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PES.Designation')),
                ('Skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PES.Skill')),
            ],
        ),
        migrations.CreateModel(
            name='SkillReview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Review', models.IntegerField()),
                ('ReviewedOn', models.DateField()),
                ('Authority', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PES.EmployeeAuthority')),
                ('Employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PES.Employee')),
                ('Skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PES.Skill')),
            ],
        ),
        migrations.AddField(
            model_name='additionalskillreview',
            name='Authority',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PES.EmployeeAuthority'),
        ),
        migrations.AddField(
            model_name='additionalskillreview',
            name='Employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PES.Employee'),
        ),
    ]
