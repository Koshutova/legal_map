from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


from legal_map.legal_help.forms import CompanyForm
from legal_map.legal_help.models import Company, MainArea


def legal_index_view(request):
    main_areas = MainArea.objects.all()

    context = {
        'main_areas': main_areas,
    }

    return render(request, 'legal_index.html', context)


def find_companies(request, pk):
    companies = Company.objects.filter(areas=pk)
    have_companies = companies.exists()
    context = {
        'companies_area': companies,
        'have_companies': have_companies,
    }
    return render(request,'companies/find_companies.html', context)


@login_required
def list_my_companies(request):
    all_companies = Company.objects.all()
    my_companies = all_companies.filter(user_id=request.user.id)
    has_company = my_companies.exists()

    context = {
        'all_companies': all_companies,
        'my_companies': my_companies,
        'has_company': has_company,
    }
    return render(request, 'companies/list_my_companies.html', context)


@login_required
def create(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES)
        if form.is_valid():
            company = form.save(commit=False)
            company.user = request.user
            company.save()
            selected_area = form.cleaned_data.get('areas')
            for area in selected_area:
                area_obj = MainArea.objects.get(name=area)
                company.areas.add(area_obj)
            return redirect('list my companies')
    else:
        form = CompanyForm()
    context = {
        'form': form,
    }
    return render(request, 'companies/company_create.html', context)


def company_details(request, pk):
    company = Company.objects.get(pk=pk)

    is_creator = company.user == request.user

    context = {
        'company': company,
        'areas': company.areas.all(),
        'is_creator': is_creator,
    }

    return render(request, 'companies/company_detail.html', context)


@login_required
def edit_company(request, pk):
    company = Company.objects.get(pk=pk)
    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES, instance=company)
        if form.is_valid():
            form.save()
            selected_area = form.cleaned_data.get('areas')
            for area in selected_area:
                area_obj = MainArea.objects.get(name=area)
                company.areas.add(area_obj)
            return redirect('list my companies')
    else:
        form = CompanyForm(instance=company)

    context = {
        'form': form,
        'company': company,
    }

    return render(request, 'companies/company_edit.html', context)


@login_required
def delete_company(request, pk):
    company = Company.objects.get(pk=pk)
    if request.method == 'POST':
        company.delete()
        return redirect('list my companies')
    else:
        context = {
            'company': company,
        }
        return render(request, 'companies/company_delete.html', context)







