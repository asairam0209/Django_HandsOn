from django.shortcuts import render
from .models import Product
from django.core.paginator import Paginator
# Create your views here.

def index(request):
    products = Product.objects.all()

#   Code for Search
    item_name = request.GET.get('item_search')
    if item_name != "" and item_name is not None:
        print(item_name)
        products = Product.objects.filter(title__icontains=item_name)

#   Code for Pagination
    paginator = Paginator(products, 3)
    page = request.GET.get('page')
    products = paginator.get_page(page)
    return render(request, 'shop/index.html', {'products': products})


def detailView(request, id):
    product = Product.objects.get(id = id)
    return render(request, 'shop/details.html', {'product': product})


def checkout(request):
    return render(request, 'shop/checkout.html')