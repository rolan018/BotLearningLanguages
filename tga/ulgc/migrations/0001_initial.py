# Generated by Django 4.2 on 2023-04-30 20:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telegram_id', models.BigIntegerField(unique=True, verbose_name='ID пользователя')),
                ('name', models.TextField(verbose_name='Имя пользователя')),
                ('telephone', models.TextField(verbose_name='Телефон пользователя')),
                ('email', models.TextField(verbose_name='Почтовый ящик пользователя')),
            ],
            options={
                'verbose_name': 'Профиль пользователя',
                'verbose_name_plural': 'Профили пользователей',
            },
        ),
        migrations.CreateModel(
            name='ActionWord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Слова пользователя')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Время действия')),
                ('telegram_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ulgc.profile', verbose_name='Профиль')),
            ],
            options={
                'verbose_name': 'Слово пользователя',
                'verbose_name_plural': 'Слова пользователя',
            },
        ),
        migrations.CreateModel(
            name='ActionMaterial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.TextField(verbose_name='Название материала')),
                ('url', models.TextField(verbose_name='Ссылка на материал')),
                ('mark', models.IntegerField(verbose_name='Оценка материала')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Время действия')),
                ('telegram_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ulgc.profile', verbose_name='Профиль')),
            ],
            options={
                'verbose_name': 'Материал пользователя',
                'verbose_name_plural': 'Материалы пользователя',
            },
        ),
        migrations.CreateModel(
            name='ActionLesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.TextField(verbose_name='Дата урока')),
                ('topic', models.TextField(verbose_name='Тема урока')),
                ('mark', models.IntegerField(verbose_name='Оценка урока')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Время действия')),
                ('telegram_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ulgc.profile', verbose_name='Профиль')),
            ],
            options={
                'verbose_name': 'Урок пользователя',
                'verbose_name_plural': 'Уроки пользователя',
            },
        ),
    ]
