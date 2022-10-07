from django.db import models


class CompanyReim(models.Model):
    """A company for invoice reimbursement"""
    company = models.CharField(max_length=30)

    def __str__(self):
        """Return a string representation of the model."""
        return self.company


class ClientReim(models.Model):
    """A client in a company"""
    company = models.ForeignKey(CompanyReim, on_delete=models.CASCADE)
    client = models.CharField(max_length=5)
    department = models.CharField(max_length=20)
    position = models.CharField(max_length=20)

    def __str__(self):
        """Return a string representation of the model."""
        return self.client


class FieldReim(models.Model):
    """A related field of a company"""
    company = models.ForeignKey(CompanyReim, on_delete=models.CASCADE)
    field = models.CharField(max_length=40)

    def __str__(self):
        """Return a string representation of the model."""
        return self.field
