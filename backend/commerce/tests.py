from django.test import TestCase

from .enums import CheckEnum
from .models import Printer, Check


class ModelTestCase(TestCase):
    fixtures = ['test_data.json', ]
    printer_1 = None
    printer_2 = None
    printer_3 = None

    def setUp(self):
        printer_1 = Printer.objects.create(name="printer 1", api_key="a", check_type=CheckEnum.TYPE_CLIENT, point_id=1)
        printer_2 = Printer.objects.create(name="printer 2", api_key="b", check_type=CheckEnum.TYPE_KITCHEN, point_id=1)
        printer_3 = Printer.objects.create(name="printer 3", api_key="c", check_type=CheckEnum.TYPE_KITCHEN, point_id=2)

        self.printer_1 = printer_1
        self.printer_2 = printer_2
        self.printer_3 = printer_3

        Check.objects.create(printer_id=printer_1, type=printer_1.check_type, order={"id": 1234},
                             status=CheckEnum.STATUS_NEW)
        Check.objects.create(printer_id=printer_2, type=printer_2.check_type, order={"id": 1234},
                             status=CheckEnum.STATUS_NEW)

    def test_get_printer(self):
        printer_1 = Printer.objects.get(name="printer 1")
        self.assertEqual(printer_1, self.printer_1)
        self.assertEqual(printer_1.check_type, CheckEnum.TYPE_CLIENT)

        printer_2 = Printer.objects.get(name="printer 2")
        self.assertEqual(printer_2, self.printer_2)
        self.assertEqual(printer_2.check_type, CheckEnum.TYPE_KITCHEN)

    def test_is_printout_checks_for_order_null(self):
        message = Printer.is_printout_checks_for_order([], 0)
        self.assertEqual(message, "Для данной точки не настроено ни одного принтера")

    def test_is_printout_checks_for_order_again(self):
        message = Printer.is_printout_checks_for_order([self.printer_1, ], 1234)
        self.assertEqual(message, "Для данного заказа уже созданы чеки")

    def test_is_printout_checks_for_order_success(self):
        message = Printer.is_printout_checks_for_order([self.printer_1, ], 12345)
        self.assertEqual(message, "")

    def test_there_is_check_file_to_print_null(self):
        message = self.printer_1.there_is_check_file_to_print(-1)
        self.assertEqual(message, "Данного чека не существует")

    def test_there_is_check_file_to_print_no_pdf(self):
        check = self.printer_1.checks.first()

        message = self.printer_1.there_is_check_file_to_print(check.id)
        self.assertEqual(message, "Для данного чека не сгенерирован PDF-файл")

    def test_there_is_check_file_to_print_success(self):
        check = self.printer_1.checks.first()
        check.status = CheckEnum.STATUS_RENDERED
        check.save()

        message = self.printer_1.there_is_check_file_to_print(check.id)
        self.assertEqual(message, "")

    def test_get_check(self):
        check_1 = self.printer_1.checks.first()
        self.assertEqual(check_1.type, CheckEnum.TYPE_CLIENT)

        check_2 = self.printer_2.checks.first()
        self.assertNotEqual(check_2.type, CheckEnum.TYPE_CLIENT)
        self.assertEqual(check_2.type, CheckEnum.TYPE_KITCHEN)

    def test_get_check_file(self):
        check = self.printer_1.checks.first()

        check.status = CheckEnum.STATUS_NEW
        check.get_file_for_print()
        self.assertEqual(check.status, CheckEnum.STATUS_NEW)

        check.status = CheckEnum.STATUS_RENDERED
        check.get_file_for_print()
        self.assertEqual(check.status, CheckEnum.STATUS_PRINTED)
