# coding=GBK
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from urllib.parse import urlencode, parse_qs

from .forms import AmountForm, RestaurantForm, DiningTypeForm, DateForm, PresetNumberForm, ConfirmForm
from .invoice_reimburse import InvoiceReimburse

@login_required
def reim_greeting(request):
    """
    prepare a page for reimbursement input, if submitted and validated, redirect to reim_outcome
    """
    if request.method != 'POST':
        # No data submitted
        amount_form = AmountForm()
        restaurant_form = RestaurantForm()
        diningtype_form = DiningTypeForm()
        date_form = DateForm()
        presetnumber_form = PresetNumberForm()
    else:
        # Post data submitted
        print("______________________________________________")
        print(request.POST)
        print("______________________________________________")
        amount_form = AmountForm(data=request.POST)
        restaurant_form = RestaurantForm(data=request.POST)
        diningtype_form = DiningTypeForm(data=request.POST)
        date_form = DateForm(data=request.POST)
        presetnumber_form = PresetNumberForm(data=request.POST)
        if restaurant_form.is_valid() and amount_form.is_valid():
            amount = request.POST.get('amount')
            restaurant = request.POST.get('restaurant')
            dining_type = request.POST.get('dining_type')
            date = request.POST.get('date')
            preset_number = request.POST.get("preset_number")
            """
            print(amount, restaurant, dining_type, date, preset_number)
            print(type(amount), type(restaurant), type(dining_type), type(date), type(preset_number))
            """
            reim_input = {
                'amount': amount,
                'restaurant': restaurant,
                'dining_type': dining_type,
                'date': date,
                'preset_number': preset_number,
            }
            reim_input = urlencode(reim_input)
            return redirect('invoice_reimbursement:reim_outcome', reim_input=reim_input)
    context = {
        'amount_form': amount_form,
        'restaurant_form': restaurant_form,
        'diningtype_form': diningtype_form,
        'date_form': date_form,
        'presetnumber_form': presetnumber_form,
    }
    return render(request, 'reim/reim_greeting.html', context)

@login_required
def reim_outcome(request, reim_input):
    """
    prepare a randomly-generated reimbursement info given the reim_input, if confirmed, generate the attachment and
    redirect to download page
    """
    reim_input = parse_qs(reim_input, keep_blank_values=True)
    #  parsing a percent encoded query string into a dict, while the values are lists, so lists should be converted to
    #  strings first
    for key in reim_input:
        reim_input[key] = reim_input[key][0]
    ir = InvoiceReimburse(reim_input)
    context = ir.who_to_dine()
    if 'confirm_and_download' in request.POST:
        ir.attachment_gen()
        return render(request, 'reim/reim_download.html')
    elif 'reroll_info' in request.POST:
        pass
    context['confirmation'] = ConfirmForm()

    return render(request, 'reim/reim_outcome.html', context)








