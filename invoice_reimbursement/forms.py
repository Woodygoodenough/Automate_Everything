# coding=GBK
from django import forms


class AmountForm(forms.Form):
    amount = forms.FloatField()


class RestaurantForm(forms.Form):
    restaurant = forms.CharField()


class DiningTypeForm(forms.Form):
    CHOICES = [
        ('工作招待', '工作招待'),
        ('一般招待', '一般招待'),
        ('商务招待', '商务招待'),
    ]
    dining_type = forms.MultipleChoiceField(choices=CHOICES)


class DateForm(forms.Form):
    date = forms.DateField()


class PresetNumberForm(forms.Form):
    preset_number = forms.IntegerField(required=False)


class ConfirmForm(forms.Form):
    confirm = forms.BooleanField(required=False)
