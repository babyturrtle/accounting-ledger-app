"""Accounting ledger views"""

from django.shortcuts import render

from .models import *
from .forms import LedgerFileForm


def file_upload(request):
    """Upload ledger file"""

    template = 'ledger.file_upload.html'
    context = {'form': LedgerFileForm()}

    if request.method == 'GET':
        return render(request, template, context)

    elif request.method == 'POST':
        used_form = LedgerFileForm(request.POST)
        if used_form.is_valid():
            pass
            return render(request, template, context)
        context['errors'] = used_form.errors

        return render(request, template, context)


def view_files(request):
    """View all uploaded files"""

    template = 'ledger.view_files.html'
    data = AccountLedger.objects.all()
    context = {'data': data}

    return render(request, template, context)


def view_ledger_file(request):
    """View information in a single ledger file"""

    template = 'ledger.view_leger_file.html'
    context = {}

    return render(request, template, context)