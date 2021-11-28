from django.db import models


class LedgerFile(models.Model):
    description = models.CharField(max_length=255, blank=True)
    file = models.FileField(upload_to='files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class AccountLedger(models.Model):
    bank = models.CharField(max_length=255)
    start_period = models.DateField()
    end_period = models.DateField()
    compiled_at = models.DateTimeField()
    ledger_file = models.ForeignKey(LedgerFile, on_delete=models.CASCADE)


class OpeningBalance(models.Model):
    active_amount = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    passive_amount = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)

    def __str__(self):
        return f'{self.active_amount}, {self.passive_amount}'

    def save(self, *args, **kwargs):
        pass


class Turnover(models.Model):
    debit_amount = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    credit_amount = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)

    def __str__(self):
        return f'{self.debit_amount}, {self.credit_amount}'

    def save(self, *args, **kwargs):
        pass


class ClosingBalance(models.Model):
    active_amount = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    passive_amount = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)

    def __str__(self):
        return f'{self.active_amount}, {self.passive_amount}'

    def save(self, *args, **kwargs):
        pass


class AccountClass(models.Model):
    number = models.PositiveIntegerField()
    name = models.CharField(max_length=200, unique=True)


class Account(models.Model):
    account_id = models.PositiveIntegerField()
    opening_balance = models.ForeignKey(OpeningBalance, on_delete=models.CASCADE)
    turnover = models.ForeignKey(Turnover, on_delete=models.CASCADE)
    closing_balance = models.ForeignKey(ClosingBalance, on_delete=models.CASCADE)
    account_class = models.ForeignKey(AccountClass, on_delete=models.CASCADE)
    account_ledger = models.ForeignKey(AccountLedger, on_delete=models.CASCADE)
