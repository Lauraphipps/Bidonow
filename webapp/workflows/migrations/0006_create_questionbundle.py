# Generated by Django 2.0.3 on 2018-03-23 13:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workflows', '0005_workflow_changes'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionBundle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),

        migrations.AlterField(
            model_name='question',
            name='workflow',
            field=models.IntegerField(default=None, null=False),
        ),

        migrations.AlterField(
            model_name='question',
            name='question_type',
            field=models.IntegerField(default=None, null=False),
        ),

        migrations.AlterField(
            model_name='workflow',
            name='id',
            field=models.IntegerField(default=None, null=False),
        ),

        migrations.AlterField(
            model_name='questiontype',
            name='id',
            field=models.IntegerField(default=None, null=False),
        ),

        migrations.AddField(
            model_name='question',
            name='bundle',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='workflows.QuestionBundle'),
            preserve_default=False,
        ),

        migrations.AddField(
            model_name='questiontype',
            name='questionbundle_ptr',
            field=models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='workflows.QuestionBundle'),
        ),

        migrations.AddField(
            model_name='workflow',
            name='questionbundle_ptr',
            field=models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='workflows.QuestionBundle'),
        ),

    ]
