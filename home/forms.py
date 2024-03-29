from django import forms
from django.contrib.auth import get_user_model

from .models import (
    Company, SeedStep, Split, SharePrice, MoneyTransaction,
    ShareTransaction, Percent, FairValueList, ShareholderList,
    Shareholder,
)
from .utils import UserChoiceField

User = get_user_model()


class CompanyForm(forms.ModelForm):

    staff = UserChoiceField(queryset=User.objects.all())
    class Meta:
        model = Company
        fields = '__all__'

class SeedStepForm(forms.ModelForm):

    class Meta:
        model = SeedStep
        widgets = {
            'start_term':forms.widgets.NumberInput(attrs={'type':'date'}),
            'end_term':forms.widgets.NumberInput(attrs={'type':'date'}),
        }
        fields = '__all__'


class SplitForm(forms.ModelForm):

    class Meta:
        model = Split
        widgets = {
            'date':forms.widgets.NumberInput(attrs={'type':'date'}),
        }
        fields = '__all__'


class SharePriceForm(forms.ModelForm):

    class Meta:
        model = SharePrice
        widgets = {
            'date':forms.widgets.NumberInput(attrs={'type':'date'}),
        }
        fields = '__all__'


class MoneyTransactionForm(forms.ModelForm):

    class Meta:
        model = MoneyTransaction
        widgets = {
            'date':forms.widgets.NumberInput(attrs={'type':'date'}),
        }
        fields = '__all__'


class ShareTransactionForm(forms.ModelForm):

    class Meta:
        model = ShareTransaction
        widgets = {
            'date':forms.widgets.NumberInput(attrs={'type':'date'}),
        }
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        transaction = cleaned_data.get('money_transaction')
        share = cleaned_data.get('share')
        if transaction and share and transaction.company != share.company:
            self._errors['share'] = self.error_class(
                ['The company of the share must match the company of the money transaction']
            )
        return cleaned_data


class PercentForm(forms.ModelForm):
    percent = forms.IntegerField(min_value=0, max_value=100)

    class Meta:
        model = Percent
        fields = '__all__'


class FairValueListForm(forms.ModelForm):

    class Meta:
        model = FairValueList
        widgets = {
            'date':forms.widgets.NumberInput(attrs={'type':'date'}),
        }
        fields = '__all__'


class ShareholderListForm(forms.ModelForm):

    class Meta:
        model = ShareholderList
        widgets = {
            'date':forms.widgets.NumberInput(attrs={'type':'date'}),
        }
        fields = '__all__'


class ShareholderForm(forms.ModelForm):

    class Meta:
        model = Shareholder
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        shareholder_list = cleaned_data.get('shareholder_list')
        share = cleaned_data.get('share')
        if shareholder_list and share and shareholder_list.company != share.company:
            self._errors['share'] = self.error_class(
                ['The company of the share must match the company of the shareholder list']
            )
        return cleaned_data