from datetime import date

from django.contrib import messages
from django.views.generic import View
from django.urls import reverse
from django.shortcuts import render, resolve_url, redirect
from django.db.models import (
    F, OuterRef, Subquery,
)

from core.settings import PORTFOLIO
from home.models import (
    Company, ContactType, Share, Shareholder, MoneyTransaction, ShareTransaction,
    SharePrice, Split,
)

from utils.pdf_utils import shareholders_from_pdf
from .forms import (
    UploadFileForm, ShareholderUploadFormSet, ShareholderExtraForm,
    CompanySelectForm, SharePriceFormSet,
)


def short_report(request):
    context = {}
    context['result_headers'] = [
        'Area', 'No. Com.', 'Pct. Com.', 'Investment', 'Investment Pct.',
        'Market Price', 'Market Price Pct.'
    ]
    sectors = {}
    locations = {}
    template = {
        'num': 0,
        'investment': 0,
        'market': 0,
    }

    # Get companies
    companies = Company.objects.filter(
        status__status = 'Portfolio'
    ).annotate(
        area = F('sector__name'),
        city = F('location__city')
    )
    total_companies = 0
    # Count companies by sector and city
    for company in companies:
        if not sectors.get(company.area):
            sectors[company.area]=template.copy()
        if not locations.get(company.city):
            locations[company.city]=template.copy()
        sectors[company.area]['num']+=1
        locations[company.city]['num']+=1
        total_companies += 1
    # Get money transactions
    money_transactions = MoneyTransaction.objects.filter(
        company__in = companies,
        portfolio__name = PORTFOLIO,
    ).annotate(
        area = F('company__sector__name'),
        city = F('company__location__city'),
        type = F('transaction_type__title'),
    )
    total_money_invested = 0
    # Sum all investments
    for transaction in money_transactions:
        if transaction.type == 'Sell':
            price = -float(transaction.price)
        else:
            price = float(transaction.price)
        total_money_invested += price
        sectors[transaction.area]['investment']+=price
        locations[transaction.city]['investment']+=price
    # Get share transactions
    share_transactions = ShareTransaction.objects.filter(
        money_transaction__company__in = companies,
    ).annotate(
        type = F('money_transaction__transaction_type__title'),
        area = F('money_transaction__company__sector__name'),
        city = F('money_transaction__company__location__city'),
    )
    total_market_price = 0
    # Sum market price
    for transaction in share_transactions:
        last_price = SharePrice.objects.filter(share=transaction.share).order_by('-date')[:1]
        splits = Split.objects.filter(
            date__gte = transaction.date,
            share=transaction.share,
        ).annotate(
            cof = F('after')/F('before'),
        ).values_list('cof')
        cof = 1
        for split in splits:
            cof *= split[0]
        if last_price.exists():
            last_price = last_price.first().price
        else:
            last_price = 0
        if transaction.type == 'Sell':
            total = -float(transaction.amount*cof*last_price)
        else:
            total = float(transaction.amount*cof*last_price)
        total_market_price += total
        sectors[transaction.area]['market']+=total
        locations[transaction.city]['market']+=total
    # Representation
    context['results_sector'] = []
    context['results_location'] = []
    context['sectors'] = []
    context['locations'] = []
    context['chart1'] = []
    context['chart2'] = []
    context['chart3'] = []
    context['chart4'] = []
    context['chart5'] = []
    context['chart6'] = []
    for key in sectors.keys():
        context['results_sector'].append((
            key, sectors[key]['num'],
            round(100/total_companies*sectors[key]['num'], 1),
            sectors[key]['investment'],
            round(100/total_money_invested*sectors[key]['investment'], 1),
            round(sectors[key]['market'], 2),
            round(100/total_market_price*sectors[key]['market'], 1),
        ))
        context['sectors'].append(key)
        context['chart1'].append(sectors[key]['num'])
        context['chart3'].append(sectors[key]['investment'])
        context['chart5'].append(sectors[key]['market'])
    for key in locations.keys():
        context['results_location'].append((
            key, locations[key]['num'], 
            round(100/total_companies*locations[key]['num'], 1),
            locations[key]['investment'],
            round(100/total_money_invested*locations[key]['investment'], 1),
            round(locations[key]['market'], 2),
            round(100/total_market_price*locations[key]['market'], 1),
        ))
        context['locations'].append(key)
        context['chart2'].append(locations[key]['num'])
        context['chart4'].append(locations[key]['investment'])
        context['chart6'].append(locations[key]['market'])
    # Footer-total
    context['footer'] = [
        'Total:', total_companies, 100, round(total_money_invested, 2),
        100, round(total_market_price, 2), 100,
    ]
    return render(request, 'pages/short_report.html', context=context)

def upload_shareholders(request):
    if request.method == "POST":
        file = request.FILES.get('file')
        company, shareholders = shareholders_from_pdf(file)
        company = Company.objects.filter(name=company).first()
        if not company or not shareholders:
            messages.error(request, 'Unsupported file type or non-existent company')
            form = UploadFileForm()
            return render(request, 'pages/simple_form.html', context={'form': form})
        initial_data = []
        special_fields = []
        for ind in range(len(shareholders)):
            contact_type = ContactType.objects.filter(contact__name=shareholders[ind][2]).first()
            if not contact_type: special_fields.append(ind)
            initial_data.append({
                'amount':shareholders[ind][0],
                'contact_type':contact_type,
                'type':shareholders[ind][1],
                'name':shareholders[ind][2],
            })
        extra_form = ShareholderExtraForm(initial={'company':company, 'date':date.today()})
        context = {
            'special_fields':special_fields,
            'title': company.name,
            'table_headers': initial_data[0].keys(),
            'formset': ShareholderUploadFormSet(initial=initial_data),
            'form_url': resolve_url('confirm_shareholders'),
            'extra_form':extra_form,
        }
        return render(request, 'pages/table_formset.html', context=context)
    else:
        form = UploadFileForm()
        context = {
            'enctype':'multipart/form-data',
            'method': "POST",
            'url': resolve_url('upload_shareholders'), 
            'form': form,
        }
        return render(request, 'pages/simple_form.html', context=context)
    

def confirm_shareholders(request):
    extra_form = ShareholderExtraForm(request.POST)
    shareholders_set_form = ShareholderUploadFormSet(request.POST)
    if not shareholders_set_form.is_valid() or not extra_form.is_valid():
        messages.error(request, 'Invalid form. Please try again.') 
        return redirect('upload_shareholders')
    for form in shareholders_set_form:
        form.save(
            company = extra_form.cleaned_data['company'],
            date = extra_form.cleaned_data['date'],
        )
    messages.success(request, 'Added successfully.')
    return redirect('short_report')

class SharePriceUpdateView(View):
    def get(self, request):
        form = CompanySelectForm(request.GET)
        if not form.is_valid():
            context = {
                'enctype':'multipart/form-data',
                'method': "GET",
                'url': resolve_url('update_prices'), 
                'form': form,
            }
            return render(request, 'pages/simple_form.html', context=context)
        shares = Share.objects.filter(company=form.cleaned_data['company'])
        initial_data = []
        for share in shares:
            initial_data.append({
                'share':share,
                'price': round(float(request.GET.get('price', 0)), 3),
                'date':  request.GET['date'] if request.GET.get('date') else date.today(),
            })
        if not initial_data: 
            messages.warning(request, 'The company has no shares')
            return redirect('update_prices')

        context = {
            'title': 'Update Price',
            'formset': SharePriceFormSet(initial=initial_data),
            'form_url': resolve_url('update_prices'),
        }
        return render(request, 'pages/table_formset.html', context=context)

    def post(self, request):
        formset = SharePriceFormSet(request.POST)
        if not formset.is_valid():
            messages.warning(request, 'Invalid form. Please try again.')
            return redirect('update_prices')
        for form in formset:
            form.save()
        return redirect('short_report')
    

class CompanyReportView(View):
    def get(self, request):
        form = CompanySelectForm(request.GET)
        if not form.is_valid():
            context = {
                'enctype':'multipart/form-data',
                'method': "GET",
                'url': resolve_url('company_report'), 
                'form': form,
            }
            return render(request, 'pages/simple_form.html', context=context)
        company = form.cleaned_data['company']
        contact = company.contact
        latest_shareholders = Shareholder.objects.filter(
            owner=OuterRef('owner')
        ).order_by('-date')

        shareholders = Shareholder.objects.annotate(
            latest_date=Subquery(latest_shareholders.values('date')[:1])
        ).filter(
            share__company=company,
            date=F('latest_date')
        )
        # Price chart
        labels = []
        datasets = {}

        shares = Share.objects.filter(
            company = company,
        )
        for share in shares:
            datasets[share.type.type] = []

        share_prices = SharePrice.objects.filter(
            share__in = shares,
        ).annotate(type = F('share__type__type')).order_by('date')

        last_date = date.min
        for share_price in share_prices:
            if share_price.date == last_date:
                datasets[share_price.type][-1] = float(share_price.price)
            else:
                labels.append(str(share_price.date))
                for key, array in datasets.items():
                    if key == share_price.type:
                        array.append(float(share_price.price))
                    else:
                        if len(array):
                            array.append(array[-1])
                        else:
                            array.append(0)
            last_date = share_price.date

        context = {
            'results':shareholders,
            'company':company,
            'contact':contact,
            'chart1':{
                'labels': labels,
                'datasets':datasets
            },
        }
        return render(request, 'pages/company_report.html', context)
    

class DetailedReportView(View):
    def get(self, request):
        res = {}
        context = {
            'result_headers':[
                'Company', 'Marshal Invested', 'Restructuring', 'Martlet Invested', 'Total Amount', 'Market Price', 'First transaction',
            ],
            'results':[],
            'links':[],
        }
        companies = Company.objects.all()
        for company in companies:
            context['links'].append(reverse('company_report')+f'?company={company.pk}')
            res[company.name] = {
                'marshal_invested': 0,
                'restructuring': 0,
                'martlet_invested': 0,
                'total_amount': 0,
                'market_price': 0,
                'first_transaction': 0,
            }

        money_transactions = MoneyTransaction.objects.all().annotate(
            type = F('transaction_type__title'),
            company_name = F('company__name'),
            portfolio_name = F('portfolio__name')
        )
        for transaction in money_transactions:
            value = transaction.price
            if transaction.type == 'Sell':
                value = -value
            if transaction.portfolio_name == 'Marshall':
                res[transaction.company_name]['marshal_invested'] += value
            elif transaction.portfolio_name == 'Martlet':
                res[transaction.company_name]['martlet_invested'] += value


        share_transactions = ShareTransaction.objects.annotate(
            company = F('share__company__name'),
            portfolio = F('money_transaction__portfolio__name'),
            type = F('money_transaction__transaction_type__title'),
        )
        for transaction in share_transactions:
            last_price = SharePrice.objects.filter(share=transaction.share).order_by('-date')[:1]
            splits = Split.objects.filter(
                date__gte = transaction.date,
                share=transaction.share,
            ).annotate(
                cof = F('after')/F('before'),
            ).values_list('cof')
            cof = 1
            for split in splits:
                cof *= split[0]
            if last_price.exists():
                last_price = last_price.first().price
            else:
                last_price = 0
            if transaction.type == 'Sell':
                res[transaction.company]['total_amount'] -= (
                    transaction.amount*cof
                )
                res[transaction.company]['market_price'] -= float(
                    transaction.amount*cof*last_price
                )
            else:
                res[transaction.company]['total_amount'] += (
                    transaction.amount*cof
                )
                res[transaction.company]['market_price'] += float(
                    transaction.amount*cof*last_price
                )
        
        for company in companies:
                restruct = MoneyTransaction.objects.filter(
                    company = company,
                    transaction_type__title = 'Restructuring',
                ).order_by('-date')[:1].first()
                if restruct:
                    res[company.name]['restructuring'] = float(restruct.price)
                else:
                    res[company.name]['restructuring'] = 0

        for company in companies:
            first_transaction = MoneyTransaction.objects.filter(
                company = company,
            ).order_by('date')[:1].first()
            if first_transaction:
                res[company.name]['first_transaction'] = first_transaction.date 
            else:
                res[company.name]['first_transaction'] = 0

        for key, value in res.items():
            context['results'].append(
                (
                    key, value['marshal_invested'], value['restructuring'],
                    value['martlet_invested'], round(value['total_amount'], 2),
                    round(value['market_price'], 2), value['first_transaction'],
                )
            )

        return render(request, 'pages/detailed_report.html', context=context)
        
