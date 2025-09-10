from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название категории")
    description = models.TextField(blank=True, verbose_name="Описание")
    color = models.CharField(max_length=7, default="#007bff", verbose_name="Цвет")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Account(models.Model):
    ACCOUNT_TYPES = (
        ('cash', 'Наличные'),
        ('card', 'Банковская карта'),
        ('credit', 'Кредитная карта'),
        ('savings', 'Сберегательный счет'),
        ('investment', 'Инвестиционный счет'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    name = models.CharField(max_length=100, verbose_name="Название счета")
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES, verbose_name="Тип счета")
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Баланс")
    currency = models.CharField(max_length=3, default="RUB", verbose_name="Валюта")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Счет"
        verbose_name_plural = "Счета"

    def __str__(self):
        return f"{self.name} ({self.account_type}) - {self.user.username}"


class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('income', 'Доход'),
        ('expense', 'Расход'),
        ('transfer', 'Перевод'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    account = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name="Счет")
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Сумма")
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES, verbose_name="Тип операции")
    status = models.CharField(max_length=50, default='OK', verbose_name="Статус операции")
    description = models.TextField(blank=True, verbose_name="Описание")
    date = models.DateField(default=timezone.now, verbose_name="Дата операции")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    time = models.TimeField(null=True, blank=True, verbose_name="Время операции")
    original_data = models.JSONField(null=True, blank=True, verbose_name="Исходные данные")

    class Meta:
        verbose_name = "Транзакция"
        verbose_name_plural = "Транзакции"
        ordering = ['-date', '-time']
