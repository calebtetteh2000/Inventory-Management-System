from django.shortcuts import render
from django.db.models import Sum, Count
from django.utils import timezone
from .models import Product, Transaction, Order

def dashboard(request):
    today = timezone.now().date()
    
    context = {
        'products_sold': Transaction.objects.filter(transaction_type='SALE', date__date=today).aggregate(Sum('quantity'))['quantity__sum'] or 0,
        'total_sales': Transaction.objects.filter(transaction_type='SALE', date__date=today).count(),
        'total_cost': Transaction.objects.filter(transaction_type='PURCHASE', date__date=today).aggregate(Sum('total_amount'))['total_amount__sum'] or 0,
        'total_amount': Transaction.objects.filter(transaction_type='SALE', date__date=today).aggregate(Sum('total_amount'))['total_amount__sum'] or 0,
    }
    
    return render(request, 'dashboard.html', context)

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})
