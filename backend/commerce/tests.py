from json import loads

from django.test import TestCase, Client
from django.urls import reverse

from .enums import CheckEnum
from .models import Printer, Check


class CommerceTestCase(TestCase):
    client = None

    fixtures = ['test_data.json', ]

    printer_1 = None
    printer_2 = None
    printer_3 = None

    def setUp(self):
        self.client = Client()

        printer_1 = Printer.objects.create(name="printer 1", api_key="a", check_type=CheckEnum.TYPE_CLIENT, point_id=1)
        printer_2 = Printer.objects.create(name="printer 2", api_key="b", check_type=CheckEnum.TYPE_KITCHEN, point_id=1)
        printer_3 = Printer.objects.create(name="printer 3", api_key="c", check_type=CheckEnum.TYPE_KITCHEN, point_id=2)

        self.printer_1 = printer_1
        self.printer_2 = printer_2
        self.printer_3 = printer_3

        Check.objects.create(printer_id=printer_1, type=printer_1.check_type, order={"id": 1234},
                             status=CheckEnum.STATUS_NEW)
        Check.objects.create(printer_id=printer_2, type=printer_2.check_type, order={"id": 1234},
                             status=CheckEnum.STATUS_RENDERED)

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
        check = self.printer_2.checks.first()
        check.save()

        message = self.printer_2.there_is_check_file_to_print(check.id)
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

    def test_url_root(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 404)

    def test_create_error_null(self):
        response = self.client.post(reverse('create'), data={'point_id': -1, 'id': -1})

        self.assertEqual(response.status_code, 400)
        message = loads(response.content)['error']
        self.assertEqual(message, 'Для данной точки не настроено ни одного принтера')

    def test_create_error_again(self):
        response = self.client.post(reverse('create'), data=dict(point_id=self.printer_1.point_id, id=1234))

        self.assertEqual(response.status_code, 400)
        message = loads(response.content)['error']
        self.assertEqual(message, 'Для данного заказа уже созданы чеки')

    def test_create_error_success(self):
        response = self.client.post(reverse('create'), data=dict(point_id=self.printer_1.point_id, id=12345))

        self.assertEqual(response.status_code, 200)
        message = loads(response.content)['ok']
        self.assertEqual(message, 'Чеки успешно созданы')

    def test_view_api_key_error(self):
        response = self.client.get(reverse('view'), data=dict(api_key='99'))

        self.assertEqual(response.status_code, 401)
        message = loads(response.content)['error']
        self.assertEqual(message, 'Ошибка авторизации')

    def test_view_success(self):
        response = self.client.get(reverse('view'), data=dict(api_key='b'))

        self.assertEqual(response.status_code, 200)
        message = loads(response.content)['checks']
        self.assertEqual(len(message) > 0, True)

    def test_print_error_check_id(self):
        response = self.client.get(reverse('print'), data=dict(api_key='b', check_id=-1))

        self.assertEqual(response.status_code, 400)
        message = loads(response.content)['error']
        self.assertEqual(message, 'Данного чека не существует')

    def test_print_error_no_pdf_file(self):
        check_id = self.printer_1.checks.filter(status=CheckEnum.STATUS_NEW).first().id
        response = self.client.get(reverse('print'), data=dict(api_key=self.printer_1.api_key, check_id=check_id))

        self.assertEqual(response.status_code, 400)
        message = loads(response.content)['error']
        self.assertEqual(message, 'Для данного чека не сгенерирован PDF-файл')

    # Для работы этого скрипта необходим сгенерированный pdf документ
    # def test_print_success(self):
    #     printer = Printer.objects.get(id=1)
    #     check_id = printer.checks.filter(status=CheckEnum.STATUS_RENDERED).first().id
    #     response = self.client.get(reverse('print'), data=dict(api_key=printer.api_key, check_id=check_id))
    #
    #     self.assertEqual(response.status_code, 200)
