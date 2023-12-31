import datetime
from typing import Any

from django import forms
from django.forms import formset_factory

from home.models import Shareholder, Share, ShareType, ContactType, Contact, Company
from home.forms import SharePriceForm

class UploadFileForm(forms.Form):
    file = forms.FileField()

class ShareholderExtraForm(forms.Form):
    company = forms.ModelChoiceField(
        queryset=Company.objects.all(),
        widget=forms.HiddenInput(),
    )
    date = forms.DateField(widget=forms.widgets.NumberInput(attrs={'type':'date'}))

class ShareholderUploadForm(forms.Form):
    name = forms.CharField()
    contact_type = forms.ModelChoiceField(
        queryset=ContactType.objects.all(),
        required=True,
        empty_label=None,
    )
    type = forms.CharField()
    amount = forms.IntegerField()
    comment = forms.CharField(max_length=10240, required=False)
    

    def save(self, company:Company, date:datetime.date):
        share_type, _ = ShareType.objects.get_or_create(type=self.cleaned_data['type'])
        share, _ = Share.objects.get_or_create(type=share_type, company=company)
        contact_type = self.cleaned_data['contact_type']
        contact = Contact.objects.filter(name=self.cleaned_data['name']).first()
        if not contact:
            contact = Contact(name=self.cleaned_data['name'])
        contact.type = contact_type
        contact.save()
        return Shareholder.objects.create(
            date = date,
            amount = self.cleaned_data['amount'],
            owner = contact,
            share = share,
            comment = self.cleaned_data['comment'],
        )
        
    
ShareholderUploadFormSet = formset_factory(ShareholderUploadForm, extra=0)

class CompanySelectForm(forms.Form):
    company = forms.ModelChoiceField(
        queryset=Company.objects.all(),
    )


class SharePriceUpdateForm(SharePriceForm):
    consider = forms.BooleanField(required=False, initial=True)

    def save(self, commit=True) -> Any:
        if self.cleaned_data.get('consider', False):
            return super().save(commit)
        return None


SharePriceFormSet = formset_factory(SharePriceUpdateForm, extra=0)