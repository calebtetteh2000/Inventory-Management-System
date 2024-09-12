from django.urls import path
from . import views

urlpatterns = [
    path('signin/', views.signin, name='signin'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', views.signup, name='signup'),
    path('products/', views.products, name='products'),
    path('logout/', views.logout_view, name='logout'),
    path('create_product/', views.create_product, name='create_product'),
    path('update_product/', views.update_product, name='update_product'),
    path('transactions/', views.transaction_list, name='transactions_list'),
    path('invoice/new/', views.new_invoice, name='invoice'),
    path('settings/', views.settings, name='settings'),
    path('help/', views.help, name='help'),
]