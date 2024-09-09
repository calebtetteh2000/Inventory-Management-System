from django.urls import path
from . import views

urlpatterns = [
    path('', views.signin, name='signin'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('signup/', views.signup, name='signup'),
    path('products/', views.products, name='products'),
    path('signout/', views.signout, name='signout'),
    path('update_product/', views.update_product, name='update_product'),
    path('transactions/', views.transaction_list, name='transaction_list')
]