# coding=GBK
from django import forms


class AmountForm(forms.Form):
    amount = forms.FloatField()


class RestaurantForm(forms.Form):
    restaurant = forms.CharField()


class DiningTypeForm(forms.Form):
    CHOICES = [
        ('�����д�', '�����д�'),
        ('һ���д�', 'һ���д�'),
        ('�����д�', '�����д�'),
    ]
    dining_type = forms.MultipleChoiceField(choices=CHOICES)


class DateForm(forms.Form):
    date = forms.DateField()


class PresetNumberForm(forms.Form):
    preset_number = forms.IntegerField(required=False)


class ConfirmForm(forms.Form):
    confirm = forms.BooleanField(required=False)
