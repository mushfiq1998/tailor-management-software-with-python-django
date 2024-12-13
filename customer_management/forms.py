from django import forms
from .models import Measurement, Order, OrderItem, CustomerFeedback

class MeasurementForm(forms.ModelForm):
    class Meta:
        model = Measurement
        exclude = ['customer', 'date_taken']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ['customer', 'order_date', 'status']
        widgets = {
            'delivery_date': forms.DateInput(attrs={'type': 'date'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        exclude = ['order']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class CustomerFeedbackForm(forms.ModelForm):
    class Meta:
        model = CustomerFeedback
        exclude = ['order', 'date_submitted']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': '1', 'max': '5'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'}) 