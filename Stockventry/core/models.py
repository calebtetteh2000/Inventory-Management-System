from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    brand_name = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='products/')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('SALE', 'Sale'),
        ('PURCHASE', 'Purchase'),
    ]
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.transaction_type} - {self.product.name} - {self.date}"

class Order(models.Model):
    ORDER_STATUS = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=ORDER_STATUS, default='PENDING')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order {self.id} - {self.user.username} - {self.date_created}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order {self.order.id}"

class Activity(models.Model):
    ACTION_TYPES = [
        ('CREATE', 'Create'),
        ('UPDATE', 'Update'),
        ('DELETE', 'Delete'),
        ('SALE', 'Sale'),
        ('PURCHASE', 'Purchase'),
        ('OTHER', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action_type = models.CharField(max_length=10, choices=ACTION_TYPES)
    target_model = models.CharField(max_length=50)  # e.g., 'Product', 'Order', etc.
    target_id = models.IntegerField()
    details = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Activities"
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user.username} - {self.action_type} {self.target_model} {self.target_id} at {self.timestamp}"

    def get_activity_description(self):
        if self.action_type == 'CREATE':
            return f"{self.user.username} added a new {self.target_model.lower()} (ID: {self.target_id})"
        elif self.action_type == 'UPDATE':
            return f"{self.user.username} updated {self.target_model.lower()} (ID: {self.target_id})"
        elif self.action_type == 'DELETE':
            return f"{self.user.username} deleted {self.target_model.lower()} (ID: {self.target_id})"
        elif self.action_type == 'SALE':
            return f"{self.user.username} made a sale (Order ID: {self.target_id})"
        elif self.action_type == 'PURCHASE':
            return f"{self.user.username} made a purchase (Order ID: {self.target_id})"
        else:
            return f"{self.user.username} performed an action on {self.target_model.lower()} (ID: {self.target_id})"