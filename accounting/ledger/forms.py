"""Accounting ledger forms"""

from django import forms
from .models import LedgerFile


class LedgerFileForm(forms.ModelForm):
    """Form for uploading files."""

    class Meta:
        model = LedgerFile

        fields = ('description', 'file',)