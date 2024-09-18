# Generated by Django 5.1 on 2024-09-18 01:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AlergiaValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=256)),
                ('normalized_value', models.CharField(editable=False, max_length=256)),
                ('state', models.CharField(choices=[('enable', 'enable'), ('disable', 'disable'), ('tocheck', 'tocheck')], default='tocheck', max_length=8)),
            ],
            options={
                'verbose_name': 'Alergia',
                'verbose_name_plural': 'Alergias',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DoencaValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=256)),
                ('normalized_value', models.CharField(editable=False, max_length=256)),
                ('state', models.CharField(choices=[('enable', 'enable'), ('disable', 'disable'), ('tocheck', 'tocheck')], default='tocheck', max_length=8)),
            ],
            options={
                'verbose_name': 'Doença',
                'verbose_name_plural': 'Doenças',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GeneroValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=256)),
                ('normalized_value', models.CharField(editable=False, max_length=256)),
                ('state', models.CharField(choices=[('enable', 'enable'), ('disable', 'disable'), ('tocheck', 'tocheck')], default='tocheck', max_length=8)),
            ],
            options={
                'verbose_name': 'Gênero',
                'verbose_name_plural': 'Gêneros',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MedicamentoValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=256)),
                ('normalized_value', models.CharField(editable=False, max_length=256)),
                ('state', models.CharField(choices=[('enable', 'enable'), ('disable', 'disable'), ('tocheck', 'tocheck')], default='tocheck', max_length=8)),
            ],
            options={
                'verbose_name': 'Medicamento',
                'verbose_name_plural': 'Medicamentos',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OrientacaoSexualValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=256)),
                ('normalized_value', models.CharField(editable=False, max_length=256)),
                ('state', models.CharField(choices=[('enable', 'enable'), ('disable', 'disable'), ('tocheck', 'tocheck')], default='tocheck', max_length=8)),
            ],
            options={
                'verbose_name': 'Orientação Sexual',
                'verbose_name_plural': 'Orientações Sexuais',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ReligiaoValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=256)),
                ('normalized_value', models.CharField(editable=False, max_length=256)),
                ('state', models.CharField(choices=[('enable', 'enable'), ('disable', 'disable'), ('tocheck', 'tocheck')], default='tocheck', max_length=8)),
            ],
            options={
                'verbose_name': 'Religião',
                'verbose_name_plural': 'Religiões',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SintomaValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=256)),
                ('normalized_value', models.CharField(editable=False, max_length=256)),
                ('state', models.CharField(choices=[('enable', 'enable'), ('disable', 'disable'), ('tocheck', 'tocheck')], default='tocheck', max_length=8)),
            ],
            options={
                'verbose_name': 'Sintoma',
                'verbose_name_plural': 'Sintomas',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TratamentoValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=256)),
                ('normalized_value', models.CharField(editable=False, max_length=256)),
                ('state', models.CharField(choices=[('enable', 'enable'), ('disable', 'disable'), ('tocheck', 'tocheck')], default='tocheck', max_length=8)),
            ],
            options={
                'verbose_name': 'Tratamento',
                'verbose_name_plural': 'Tratamentos',
                'abstract': False,
            },
        ),
    ]
