import os

import requests
from django.conf import settings
from django.core.files.base import ContentFile
from django.template.response import SimpleTemplateResponse

from .enums import CheckEnum


def generate_check_file(check):
    pdf_file_path = f'pdf/{check.order["id"]}_{check.type}.pdf'

    if os.path.isfile(pdf_file_path):
        return Exception

    response = requests.post(url=settings.HTML2PDF_URL,
                             files={'file': _get_file_content(_get_file_name(check), check)})

    _add_pdf_from_check_model(check, pdf_file_path, response.content)


def _get_file_name(check):
    return 'client_check.html' if check.type == CheckEnum.TYPE_CLIENT else 'kitchen_check.html'


def _get_file_content(template_path, check_data):
    return SimpleTemplateResponse(template_path, {"check": check_data}).rendered_content


def _add_pdf_from_check_model(check, file_path, check_data):
    check.status = CheckEnum.STATUS_RENDERED
    check.pdf_file.save(name=file_path, content=ContentFile(check_data), save=True)
