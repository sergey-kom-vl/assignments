from django.db import models
from .enums import CheckEnum
from django.contrib.postgres.fields import JSONField


class Point(models.Model):
    class Meta:
        verbose_name = 'Точка продажы'
        verbose_name_plural = 'Точки продажи'

    name = models.CharField(max_length=50, unique=True, verbose_name="Название")

    def __str__(self):
        return f"<Point: name {self.name}>"


class Printer(models.Model):
    class Meta:
        verbose_name = 'Принтер'
        verbose_name_plural = 'Принтеры'

    name = models.CharField(max_length=50, unique=True, verbose_name="Название")
    api_key = models.CharField(max_length=100, unique=True, verbose_name="Ключ доступа к API")
    check_type = models.CharField(max_length=10, choices=CheckEnum.CHECK_TYPE, verbose_name="Тип печатаемого чека")

    point_id = models.ForeignKey(Point, on_delete=models.CASCADE, verbose_name="Привязанная точка")

    def __str__(self):
        return f"<Printer: name {self.name}>"


class Check(models.Model):
    class Meta:
        verbose_name = 'Чек'
        verbose_name_plural = 'Чеки'

    printer_id = models.ForeignKey(Printer, on_delete=models.CASCADE, verbose_name="Принтер")

    type = models.CharField(max_length=10, choices=CheckEnum.CHECK_TYPE, verbose_name="Тип чека")
    order = JSONField(verbose_name="Информация о заказе")
    status = models.CharField(max_length=10, choices=CheckEnum.CHECK_STATUS, verbose_name="Статус чека")
    pdf_file = models.FileField(verbose_name="Cсылка на PDF-файл")

    def __str__(self):
        return f"<Check: type {self.type}, status: {self.status}>"
