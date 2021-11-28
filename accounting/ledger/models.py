"""Accounting ledger models"""

from django.db import models


class AccountLedger(models.Model):
    description = models.CharField(max_length=255, blank=True)
    file = models.FileField(upload_to='files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    bank = models.CharField(max_length=255)
    start_period = models.DateField()
    end_period = models.DateField()
    compiled_at = models.DateTimeField()


class AccountClass(models.Model):
    number = models.PositiveIntegerField()
    name = models.CharField(max_length=200, unique=True)


class OpeningBalance(models.Model):
    active_amount = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    passive_amount = models.DecimalField(max_digits=20, decimal_places=4, default=0)


class Turnover(models.Model):
    debit_amount = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    credit_amount = models.DecimalField(max_digits=20, decimal_places=4, default=0)


class ClosingBalance(models.Model):
    active_amount = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    passive_amount = models.DecimalField(max_digits=20, decimal_places=4, default=0)


class Account(models.Model):
    account_id = models.PositiveIntegerField()
    opening_balance = models.ForeignKey(OpeningBalance, on_delete=models.CASCADE)
    turnover = models.ForeignKey(Turnover, on_delete=models.CASCADE)
    closing_balance = models.ForeignKey(ClosingBalance, on_delete=models.CASCADE)
    account_class = models.ForeignKey(AccountClass, on_delete=models.CASCADE)
    account_ledger = models.ForeignKey(AccountLedger, on_delete=models.CASCADE)
