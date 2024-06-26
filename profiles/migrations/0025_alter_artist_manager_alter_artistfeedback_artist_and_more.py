# Generated by Django 5.0.6 on 2024-06-25 11:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('misc', '0001_initial'),
        ('profiles', '0024_project_visibility'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='manager',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_to_Manager_relation', to='profiles.manager'),
        ),
        migrations.AlterField(
            model_name='artistfeedback',
            name='artist',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_Artist', to='profiles.artist'),
        ),
        migrations.AlterField(
            model_name='artistrequest',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_Location', to='misc.location'),
        ),
        migrations.AlterField(
            model_name='artistrequest',
            name='rejected_artists',
            field=models.ManyToManyField(default='', related_name='%(class)s_RejectedArtist', to='profiles.artist'),
        ),
        migrations.AlterField(
            model_name='artistrequest',
            name='shortlisted_artists',
            field=models.ManyToManyField(default='', related_name='%(class)s_ShortlistedArtist', to='profiles.artist'),
        ),
        migrations.AlterField(
            model_name='artistrequest',
            name='skill',
            field=models.ManyToManyField(blank=True, default='', related_name='%(class)s_Skill', to='misc.skill'),
        ),
        migrations.AlterField(
            model_name='project',
            name='assigned_artists',
            field=models.ManyToManyField(blank=True, default='', related_name='%(class)s_AssignedArtist', to='profiles.artist'),
        ),
        migrations.AlterField(
            model_name='project',
            name='client',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_Artist', to='profiles.client'),
        ),
        migrations.AlterField(
            model_name='project',
            name='project_demos',
            field=models.ManyToManyField(blank=True, default='', related_name='%(class)s_ProjectDemo', to='profiles.projectdemo'),
        ),
        migrations.AlterField(
            model_name='project',
            name='project_template',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_to_TemplateProjects_relation', to='profiles.templateprojects'),
        ),
        migrations.AlterField(
            model_name='project',
            name='shortlisted_artists',
            field=models.ManyToManyField(blank=True, default='', related_name='%(class)s_shortlistedArtist', to='profiles.artist'),
        ),
        migrations.AlterField(
            model_name='projectdemo',
            name='artist',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_Artist', to='profiles.artist'),
        ),
        migrations.AlterField(
            model_name='projectdemo',
            name='demo_work',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_DemoWork', to='profiles.work'),
        ),
        migrations.AlterField(
            model_name='projectdemo',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_Project', to='profiles.project'),
        ),
        migrations.AlterField(
            model_name='templateprojects',
            name='skills',
            field=models.ManyToManyField(blank=True, related_name='%(class)s_Skill', through='profiles.TemplateProjectSkill', to='misc.skill'),
        ),
        migrations.AlterField(
            model_name='work',
            name='owner',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_Artist', to='profiles.artist'),
        ),
    ]
