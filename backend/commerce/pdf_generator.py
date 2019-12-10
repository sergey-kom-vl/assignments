import os

import requests
from django.conf import settings
from django.core.files.base import ContentFile
from django.shortcuts import render

from .enums import CheckEnum
from .models import Check


async def generate_check_file(request, data):
    pdf_file_path = f'pdf/{data["id"]}_{data["type"]}.pdf'

    if os.path.isfile(pdf_file_path):
        return Exception

    response = requests.post(url=settings.WKHTMLTOPDF_URL,
                             files={'file': render(request, get_file_name(data), data).content})

    # file_write(pdf_file_path, response.content)
    add_pdf_from_check_model(int(data["id"]), pdf_file_path, response.content)


def get_file_name(data):
    return 'client_check.html' if data["type"] == CheckEnum.TYPE_CLIENT else 'kitchen_check.html'


def file_write(path, data):
    with open(path, "wb") as file:
        file.write(data)


def add_pdf_from_check_model(check_id, file_path, data):
    check = Check.objects.get(id=check_id)
    check.pdf_file.save(name=file_path, content=ContentFile(data), save=True)
