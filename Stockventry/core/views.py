from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from django.utils import timezone
from .models import Product, Transaction, Order, Activity, OrderItem
from django.contrib.auth import authenticate, login, logout
from django.db import transaction
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .forms import CustomUserCreationForm, ProductForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .forms import UserProfileForm

def dashboard(request):
    today = timezone.now().date()
    recent_activities = Activity.objects.all()[:10]
    
    context = {
        'products_sold': Transaction.objects.filter(transaction_type='SALE', date__date=today).aggregate(Sum('quantity'))['quantity__sum'] or 0,
        'total_sales': Transaction.objects.filter(transaction_type='SALE', date__date=today).count(),
        'total_cost': Transaction.objects.filter(transaction_type='PURCHASE', date__date=today).aggregate(Sum('total_amount'))['total_amount__sum'] or 0,
        'total_amount': Transaction.objects.filter(transaction_type='SALE', date__date=today).aggregate(Sum('total_amount'))['total_amount__sum'] or 0,
        'recent_activities': recent_activities,
    }
    
    return render(request, 'dashboard.html', context)

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

# @login_required
def create_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        category = request.POST.get('category')
        price = request.POST.get('price')
        brand_name = request.POST.get('brand_name')
        cost = request.POST.get('cost')
        quantity = request.POST.get('quantity')

        new_product = Product.objects.create(
            name=name,
            category_id=category,  # Assuming category is passed as an ID
            price=price,
            brand_name=brand_name,
            cost=cost,
            quantity=quantity,
            user=request.user
        )

        # Log activity
        Activity.objects.create(
            user=request.user,
            action_type='CREATE',
            target_model='Product',
            target_id=new_product.id,
            details=f"Created product: {new_product.name}"
        )

        return redirect('product_list')

    return render(request, 'create_product.html')

# @login_required
def update_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.category_id = request.POST.get('category')
        product.price = request.POST.get('price')
        product.brand_name = request.POST.get('brand_name')
        product.cost = request.POST.get('cost')
        product.quantity = request.POST.get('quantity')
        product.save()

        # Log activity
        Activity.objects.create(
            user=request.user,
            action_type='UPDATE',
            target_model='Product',
            target_id=product.id,
            details=f"Updated product: {product.name}"
        )

        return redirect('product_list')

    return render(request, 'update_product.html', {'product': product})

# @login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':  # Assuming deletion is confirmed via a POST request
        # Log activity before deleting the product
        Activity.objects.create(
            user=request.user,
            action_type='DELETE',
            target_model='Product',
            target_id=product.id,
            details=f"Deleted product: {product.name}"
        )

        product.delete()
        return redirect('product_list')

    return render(request, 'delete_product.html', {'product': product})

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

# @login_required
def products(request):
    products = Product.objects.all()
    return render(request, 'product.html', {'products': products})

def signin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid email or password')
    return render(request, 'signin.html')

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect('login')  # Redirect to your login page

# @login_required
# def create_product(request):
#     if request.method == 'POST':
#         form = ProductForm(request.POST)
#         if form.is_valid():
#             product = form.save(commit=False)
#             product.user = request.user
#             product.save()

#             # Log activity
#             Activity.objects.create(
#                 user=request.user,
#                 action_type='CREATE',
#                 target_model='Product',
#                 target_id=product.id,
#                 details=f"Created product: {product.name}"
#             )

#             return redirect('product_list')
#     else:
#         form = ProductForm()

#     return render(request, 'create_product.html', {'form': form})

def transaction_list(request):
    transactions = Transaction.objects.all().order_by('-date')
    context = {
        'transactions': transactions,
    }
    return render(request, 'transaction_list.html', context)

@login_required
def new_invoice(request):
    if request.method == 'POST':
        with transaction.atomic():
            # Process the form data and create a new order
            order = Order.objects.create(
                user=request.user,
                status='PENDING',
                total_amount=0,
                payment_method=request.POST.get('payment_method', 'CASH')
            )

            # Process each item in the order
            total_amount = 0
            for key, value in request.POST.items():
                if key.startswith('product_') and value:
                    product_id = int(value)
                    quantity = int(request.POST.get(f'quantity_{product_id}', 0))
                    if quantity > 0:
                        product = Product.objects.get(id=product_id)
                        OrderItem.objects.create(
                            order=order,
                            product=product,
                            quantity=quantity,
                            price=product.price
                        )
                        total_amount += product.price * quantity

            # Update the total amount and save the order
            order.total_amount = total_amount
            order.save()

        return redirect('invoice_detail', order_id=order.id)

    # If it's a GET request, render the new invoice form
    products = Product.objects.filter(quantity__gt=0)
    context = {
        'products': products,
        'invoice_id': Order.objects.count() + 1,  # Simple way to generate a new invoice ID
        'current_date': timezone.now().date(),
        'current_time': timezone.now().time(),
        'user': request.user,
    }
    return render(request, 'new_invoice.html', context)

@login_required
def settings(request):
    if request.method == 'POST':
        user_form = UserProfileForm(request.POST, instance=request.user)
        password_form = PasswordChangeForm(request.user, request.POST)
        if 'update_profile' in request.POST:
            if user_form.is_valid():
                user_form.save()
                messages.success(request, 'Your profile was successfully updated!')
                return redirect('settings')
        elif 'change_password' in request.POST:
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Your password was successfully updated!')
                return redirect('settings')
    else:
        user_form = UserProfileForm(instance=request.user)
        password_form = PasswordChangeForm(request.user)
    
    context = {
        'user_form': user_form,
        'password_form': password_form,
    }
    return render(request, 'settings.html', context)

@login_required
def help(request):
    faqs = [
        {
            'question': 'How do I add a new product?',
            'answer': 'To add a new product, go to the Products page and click on the "Add New Product" button. Fill in the required information and click "Save".'
        },
        {
            'question': 'How can I view my transaction history?',
            'answer': 'You can view your transaction history by navigating to the Transaction page. Here, you\'ll find a list of all your past transactions, including sales and purchases.'
        },
        {
            'question': 'How do I generate an invoice?',
            'answer': 'To generate an invoice, go to the Invoice page and click on "New Invoice". Select the products, enter the quantities, and add customer information. Then click "Generate Invoice".'
        },
        {
            'question': 'How can I update my stock levels?',
            'answer': 'Stock levels are automatically updated when you record sales or purchases. You can also manually adjust stock levels on the Products page by editing a specific product.'
        },
        {
            'question': 'How do I change my account password?',
            'answer': 'To change your password, go to the Settings page. Scroll down to the "Change Password" section, enter your current password and your new password, then click "Change Password".'
        }
    ]
    return render(request, 'help.html', {'faqs': faqs})