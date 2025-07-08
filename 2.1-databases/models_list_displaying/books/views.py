from django.shortcuts import render, redirect, get_object_or_404
from .models import Phone

def index(request):
    return redirect('catalog')


def show_catalog(request):
    sort_param = request.GET.get('sort')
    phones = Phone.objects.all()

    if sort_param in ['name', 'price', '-price']:
        phones = phones.order_by(sort_param)

    return render(request, 'catalog.html', {'phones': phones})


def show_product(request, slug):
    phone = get_object_or_404(Phone, slug=slug)
    return render(request, 'product.html', {'phone': phone})