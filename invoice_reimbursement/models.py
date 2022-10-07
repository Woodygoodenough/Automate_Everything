from django.db import models


class CompanyReim(models.Model):
    """A company for invoice reimbursement"""
    company = models.CharField(max_length=30)


class ClientReim(models.Model):
    """A client in a company"""
    company = models.ForeignKey(CompanyReim, on_delete=models.CASCADE)
    client = models.CharField(max_length=5)
    department = models.CharField(max_length=20)
    position = models.CharField(max_length=20)


class FieldReim(models.Model):
    """A related field of a company"""
    company = models.ForeignKey(CompanyReim, on_delete=models.CASCADE)
    field = models.CharField(max_length=40)
