from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Product, Category

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500',
        'placeholder': 'First Name'
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500',
        'placeholder': 'Last Name'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500',
        'placeholder': 'Email'
    }))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500',
        'placeholder': 'Phone Number'
    }))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'phone_number', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500',
            'placeholder': 'Username'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500',
            'placeholder': 'Password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500',
            'placeholder': 'Confirm Password'
        })

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'cost', 'price', 'quantity', 'image', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50', 'placeholder': 'Enter Name'}),
            'category': forms.Select(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50', 'placeholder': 'Enter Category'}),
            'cost': forms.NumberInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50', 'placeholder': 'Enter Cost'}),
            'price': forms.NumberInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50', 'placeholder': 'Enter Price'}),
            'quantity': forms.NumberInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50', 'placeholder': 'Enter Quantity'}),
            'image': forms.FileInput(attrs={'class': 'mt-1 block w-full'}),
            'description': forms.Textarea(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50', 'rows': 3}),
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'w-full p-2 border rounded'})
