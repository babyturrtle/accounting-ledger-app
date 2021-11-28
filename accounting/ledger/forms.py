"""Accounting ledger forms"""

from django import forms
from .models import AccountLedger


class LedgerFileForm(forms.ModelForm):
    """Form for uploading files."""

    class Meta:
        model = AccountLedger
        fields = ('file',)
