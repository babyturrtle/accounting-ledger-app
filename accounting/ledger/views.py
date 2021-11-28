"""Accounting ledger views"""

from django.shortcuts import render

from .models import *
from .forms import LedgerFileForm
from .utils import get_ledger_info, read_excel


def file_upload(request):
    """Upload ledger file"""

    template = 'ledger.file_upload.html'
    context = {'form': LedgerFileForm()}

    if request.method == 'GET':
        return render(request, template, context)

    elif request.method == 'POST':
        form = LedgerFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, template, context)
        context['errors'] = form.errors

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