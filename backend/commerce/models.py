from django.contrib.postgres.fields import JSONField
from django.db import models
from django_rq import enqueue as rq_enqueue

from .enums import CheckEnum
from .tasks import generate_check_file


class Printer(models.Model):
    class Meta:
        verbose_name = 'Принтер'
        verbose_name_plural = 'Принтеры'

    name = models.CharField(max_length=50, unique=True, verbose_name="Название")
    api_key = models.CharField(max_length=100, unique=True, verbose_name="Ключ доступа к API")
    check_type = models.CharField(max_length=10, choices=CheckEnum.CHECK_TYPE, verbose_name="Тип печатаемого чека")

    point_id = models.IntegerField(verbose_name="Привязанная точка")

    def __str__(self):
        return self.name

    @classmethod
    def create_checks(cls, printers, order_data):
        for printer in printers:
            printer.create_check(order_data=order_data)

    def create_check(self, order_data):
        check = Check(printer_id=self,
                      type=self.check_type,
                      order=order_data,
                      status=CheckEnum.STATUS_NEW)

        check.save()
        rq_enqueue(generate_check_file, check)

    @classmethod
    def is_printout_checks_for_order(cls, printers, order_id):
        if len(printers) == 0:
            return "Для данной точки не настроено ни одного принтера"
        elif sum(printer.checks.filter(order__id=order_id).count() for printer in printers) > 0:
            return "Для данного заказа уже созданы чеки"

        return ""

    def there_is_check_file_to_print(self, check_id):
        check = self.checks.filter(id=check_id)

        if len(check) == 0:
            return "Данного чека не существует"
        elif check[0].status == CheckEnum.STATUS_NEW:
            return "Для данного чека не сгенерирован PDF-файл"

        return ""


class Check(models.Model):
    class Meta:
        verbose_name = 'Чек'
        verbose_name_plural = 'Чеки'

    printer_id = models.ForeignKey(Printer, related_name='checks', on_delete=models.CASCADE, verbose_name="Принтер")

    type = models.CharField(max_length=10, choices=CheckEnum.CHECK_TYPE, verbose_name="Тип чека")
    order = JSONField(verbose_name="Информация о заказе")
    status = models.CharField(max_length=10, choices=CheckEnum.CHECK_STATUS, verbose_name="Статус чека")
    pdf_file = models.FileField(verbose_name="Cсылка на PDF-файл", null=True)

    def __str__(self):
        return f"Чек №{self.id}"

    def get_file_for_print(self):
        if self.status != CheckEnum.STATUS_PRINTED:
            self.status = CheckEnum.STATUS_PRINTED
            self.save()

        return self.pdf_file
