"""Defining urls for invoice reimbursement"""
from django.urls import path
from . import views

app_name = 'invoice_reimbursement'
urlpatterns = [
    # Homepage for invoice reimbursement
    path('', views.reim_greeting, name='reim_greeting'),
    path('outcome/<str:reim_input>', views.reim_outcome, name='reim_outcome'),
    path('download/<str:attach_name>', views.attach_download, name='reim_download')
]
