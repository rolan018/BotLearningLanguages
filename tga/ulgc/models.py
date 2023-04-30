"""
Модели объектов в базе данных телеграмм-бота
"""
from django.db import models


class Profile(models.Model):
    """
    Профиль пользователя бота
    """
    telegram_id = models.BigIntegerField(verbose_name='ID пользователя',
                                         unique=True)
    name = models.TextField(verbose_name='Имя пользователя')
    telephone = models.TextField(verbose_name='Телефон пользователя')
    email = models.TextField(verbose_name='Почтовый ящик пользователя')

    # Для более читаемого вывода
    def __str__(self):
        return f"{self.telegram_id}"

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'


class ActionWord(models.Model):
    """
    Сообщения пользователя
    """
    telegram_id = models.ForeignKey(
        to='ulgc.Profile',
        verbose_name='Профиль',
        on_delete=models.PROTECT,
    )
    text = models.TextField(
        verbose_name='Слова пользователя'
    )
    created_at = models.DateTimeField(
        verbose_name='Время действия',
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.telegram_id}, {self.text}"

    class Meta:
        verbose_name = "Слово пользователя"
        verbose_name_plural = "Слова пользователя"


class ActionMaterial(models.Model):
    """
    Материалы пользователя
    """
    telegram_id = models.ForeignKey(
        to='ulgc.Profile',
        verbose_name='Профиль',
        on_delete=models.PROTECT,
    )
    topic = models.TextField(
        verbose_name='Название материала'
    )
    url = models.TextField(
        verbose_name='Ссылка на материал'
    )
    mark = models.IntegerField(
        verbose_name='Оценка материала'
    )
    created_at = models.DateTimeField(
        verbose_name='Время действия',
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.telegram_id}, {self.text}"

    class Meta:
        verbose_name = "Материал пользователя"
        verbose_name_plural = "Материалы пользователя"


class ActionLesson(models.Model):
    """
    Уроки пользователя
    """
    telegram_id = models.ForeignKey(
        to='ulgc.Profile',
        verbose_name='Профиль',
        on_delete=models.PROTECT,
    )
    date = models.TextField(
        verbose_name='Дата урока'
    )
    topic = models.TextField(
        verbose_name='Тема урока'
    )
    mark = models.IntegerField(
        verbose_name='Оценка урока'
    )
    created_at = models.DateTimeField(
        verbose_name='Время действия',
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.telegram_id}, {self.text}"

    class Meta:
        verbose_name = "Урок пользователя"
        verbose_name_plural = "Уроки пользователя"