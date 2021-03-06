# Generated by Django 3.1.4 on 2020-12-21 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizz', '0002_auto_20170725_1902'),
    ]

    operations = [
        migrations.CreateModel(
            name='Verb',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kana', models.CharField(default='', max_length=30)),
                ('kanji', models.CharField(blank=True, default='', max_length=30)),
                ('neutre_present', models.CharField(default='', max_length=40)),
                ('neutre_passe', models.CharField(default='', max_length=40)),
                ('neutre_present_neg', models.CharField(default='', max_length=40)),
                ('neutre_passe_neg', models.CharField(default='', max_length=40)),
                ('poli_present', models.CharField(default='', max_length=40)),
                ('poli_passe', models.CharField(default='', max_length=40)),
                ('poli_present_neg', models.CharField(default='', max_length=40)),
                ('poli_passe_neg', models.CharField(default='', max_length=40)),
                ('forme_te', models.CharField(default='', max_length=40)),
                ('forme_passive', models.CharField(default='', max_length=40)),
                ('cond_tara', models.CharField(default='', max_length=40)),
                ('cond_eba', models.CharField(default='', max_length=40)),
                ('factitif', models.CharField(default='', max_length=40)),
                ('potentiel', models.CharField(default='', max_length=40)),
                ('volitive', models.CharField(default='', max_length=40)),
                ('suspensive', models.CharField(default='', max_length=40)),
                ('poli_conjectural', models.CharField(default='', max_length=40)),
                ('gerondif', models.CharField(default='', max_length=40)),
                ('imperatif', models.CharField(default='', max_length=40)),
                ('imperatif_neg', models.CharField(default='', max_length=40)),
                ('imperatif_sup', models.CharField(default='', max_length=40)),
                ('imperatif_neg_sup', models.CharField(default='', max_length=40)),
                ('imperatif_poli', models.CharField(default='', max_length=40)),
                ('imperatif_poli_neg', models.CharField(default='', max_length=40)),
            ],
        ),
    ]
