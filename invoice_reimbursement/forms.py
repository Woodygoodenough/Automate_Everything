from django import forms


class AmountForm(forms.Form):
    amount = forms.FloatField()

class RestaurantForm(forms.Form):
    restaurant = forms.CharField()

class DateForm(forms.Form):
    date = forms.DateField()

class PresetFlagForm(forms.Form):
    preset_flag = forms.BooleanField(required=False)

class PresetNumberForm(forms.Form):
    preset_number = forms.IntegerField()

class ConfirmForm(forms.Form):
    confirm = forms.BooleanField(required=False)
