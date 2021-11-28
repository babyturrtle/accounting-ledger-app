"""Accounting ledger views"""

from django.shortcuts import render
import xlrd
import re
from datetime import datetime

from .models import *
from .forms import LedgerFileForm


def file_upload(request):
    """Uploads ledger file and adds its contents to the database"""

    template = 'ledger.file_upload.html'
    context = {'form': LedgerFileForm()}

    if request.method == 'GET':
        return render(request, template, context)

    elif request.method == 'POST':
        form = LedgerFileForm(request.POST, request.FILES)
        if form.is_valid():
            ledger_object = form.save(commit=False)
            sheet = xlrd.open_workbook(ledger_object.file).sheet_by_index(0)
            sheet.cell_value(0, 0)

            dates = re.findall(r'\d{2}\.\d{2}\.\d{4}', sheet.cell(2, 0).value)

            ledger_object.bank = sheet.cell(0, 0).value
            ledger_object.description = " ".join([
                sheet.cell_value(1, 0),
                sheet.cell_value(2, 0),
                sheet.cell_value(3, 0)
            ])
            ledger_object.compiled_at = xlrd.xldate_as_datetime(sheet.cell(5, 0).value, 0)
            ledger_object.start_period = datetime.strptime(dates[0], '%d.%m.%Y').date()
            ledger_object.end_period = datetime.strptime(dates[1], '%d.%m.%Y').date()
            ledger_object.save()

            return render(request, template, context)
        context['errors'] = form.errors

        return render(request, template, context)


def view_files(request):
    """View all uploaded files"""

    template = 'ledger.view_files.html'
    data = AccountLedger.objects.all()
    context = {'data': data}

    return render(request, template, context)


def view_ledger_file(request, file_id):
    """View information in a single ledger file"""

    template = 'ledger.view_leger_file.html'
    account_ledger = AccountLedger.objects.get(pk=file_id)
    context = {"account_ledger": account_ledger}

    return render(request, template, context)
