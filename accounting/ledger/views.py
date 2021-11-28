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
            # Create an AccountLedger object
            ledger_object = form.save(commit=False)
            sheet = xlrd.open_workbook(ledger_object.file).sheet_by_index(0)
            sheet.cell_value(0, 0)

            dates = re.findall(r'\d{2}\.\d{2}\.\d{4}', sheet.cell(2, 0).value)

            ledger_object.bank = sheet.cell(0, 0).value
            ledger_object.description = " ".join([
                sheet.cell_value(1, 0),
                sheet.cell_value(2, 0),
                sheet.cell_value(3, 0)])
            ledger_object.compiled_at = xlrd.xldate_as_datetime(sheet.cell(5, 0).value, 0)
            ledger_object.start_period = datetime.strptime(dates[0], '%d.%m.%Y').date()
            ledger_object.end_period = datetime.strptime(dates[1], '%d.%m.%Y').date()
            ledger_object.save()

            # Create AccountClass and Account objects
            for row in range(8, sheet.nrows):
                if sheet.cell_type(row, 1) == 0:
                    class_object = AccountClass(
                        name=re.compile(r'^КЛАСС  \d  (.*)$').search(sheet.cell(row, 0).value).group(1),
                        number=re.search(r'\d', sheet.cell(row, 0).value).group(0))
                    class_object.save()
                if sheet.cell_type(row, 1) != 0 and len(str(sheet.cell(row, 0).value)) == 4:
                    op_balance_object = OpeningBalance(
                        active_amount=sheet.cell(row, 1).value,
                        passive_amount=sheet.cell(row, 2).value)
                    op_balance_object.save()
                    turnover_object = Turnover(
                        debit_amount=sheet.cell(row, 3).value,
                        credit_amount=sheet.cell(row, 4).value)
                    turnover_object.save()
                    cl_balance_object = ClosingBalance(
                        active_amount=sheet.cell(row, 5).value,
                        passive_amount=sheet.cell(row, 6).value)
                    cl_balance_object.save()
                    account_object = Account(
                        account_id=int(sheet.cell(row, 0).value),
                        opening_balance=op_balance_object,
                        turnover=turnover_object,
                        closing_balance=cl_balance_object,
                        account_class=AccountClass.objects.get(number=int(str(sheet.cell(row, 0).value)[:1])),
                        account_ledger=ledger_object)
                    account_object.save()

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
    account_ledger = AccountLedger.objects.get(id=file_id)
    accounts = account_ledger.account_set.all()
    context = {"account_ledger": account_ledger, "accounts": accounts}

    return render(request, template, context)
