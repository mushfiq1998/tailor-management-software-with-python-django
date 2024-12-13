from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import (
    Measurement, Order, OrderItem, CustomerFeedback, 
    CustomerNotification
)
from .forms import (
    MeasurementForm, OrderForm, OrderItemForm, 
    CustomerFeedbackForm
)

@login_required
def measurement_list(request):
    measurements = Measurement.objects.filter(customer=request.user).order_by('-date_taken')
    return render(request, 'customer_management/measurement_list.html', {
        'measurements': measurements
    })

@login_required
def measurement_create(request):
    if request.method == 'POST':
        form = MeasurementForm(request.POST)
        if form.is_valid():
            measurement = form.save(commit=False)
            measurement.customer = request.user
            measurement.save()
            messages.success(request, 'Measurements saved successfully!')
            return redirect('customer_management:measurement_list')
    else:
        form = MeasurementForm()
    
    return render(request, 'customer_management/measurement_form.html', {
        'form': form,
        'title': 'Add New Measurements'
    })

@login_required
def order_list(request):
    orders = Order.objects.filter(customer=request.user).order_by('-order_date')
    return render(request, 'customer_management/order_list.html', {
        'orders': orders
    })

@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk, customer=request.user)
    return render(request, 'customer_management/order_detail.html', {
        'order': order
    })

@login_required
def order_create(request):
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        item_form = OrderItemForm(request.POST)
        if order_form.is_valid() and item_form.is_valid():
            order = order_form.save(commit=False)
            order.customer = request.user
            order.save()
            
            item = item_form.save(commit=False)
            item.order = order
            item.save()
            
            # Send notification
            notification = CustomerNotification.objects.create(
                customer=request.user,
                notification_type='ORDER_STATUS',
                title='New Order Created',
                message=f'Your order #{order.id} has been created successfully.'
            )
            
            # Send email
            send_mail(
                'Order Confirmation',
                f'Your order #{order.id} has been created successfully.',
                settings.DEFAULT_FROM_EMAIL,
                [request.user.email],
                fail_silently=True,
            )
            
            messages.success(request, 'Order created successfully!')
            return redirect('order_detail', pk=order.pk)
    else:
        order_form = OrderForm()
        item_form = OrderItemForm()
    
    return render(request, 'customer_management/order_form.html', {
        'order_form': order_form,
        'item_form': item_form
    })

@login_required
def feedback_create(request, order_pk):
    order = get_object_or_404(Order, pk=order_pk, customer=request.user)
    
    if request.method == 'POST':
        form = CustomerFeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.order = order
            feedback.save()
            messages.success(request, 'Thank you for your feedback!')
            return redirect('customer_management:order_detail', pk=order.pk)
    else:
        form = CustomerFeedbackForm()
    
    return render(request, 'customer_management/feedback_form.html', {
        'form': form,
        'order': order
    })

@login_required
def notification_list(request):
    notifications = CustomerNotification.objects.filter(
        customer=request.user
    ).order_by('-date_sent')
    return render(request, 'customer_management/notification_list.html', {
        'notifications': notifications
    })

@login_required
def measurement_edit(request, pk):
    measurement = get_object_or_404(Measurement, pk=pk, customer=request.user)
    
    if request.method == 'POST':
        form = MeasurementForm(request.POST, instance=measurement)
        if form.is_valid():
            form.save()
            messages.success(request, 'Measurements updated successfully!')
            return redirect('customer_management:measurement_list')
    else:
        form = MeasurementForm(instance=measurement)
    
    return render(request, 'customer_management/measurement_form.html', {
        'form': form,
        'title': 'Edit Measurements'
    })

@login_required
def measurement_delete(request, pk):
    measurement = get_object_or_404(Measurement, pk=pk, customer=request.user)
    
    if request.method == 'POST':
        measurement.delete()
        messages.success(request, 'Measurements deleted successfully!')
        return redirect('customer_management:measurement_list')
    
    return redirect('customer_management:measurement_list')

@login_required
def order_edit(request, pk):
    order = get_object_or_404(Order, pk=pk, customer=request.user)
    
    if request.method == 'POST':
        order_form = OrderForm(request.POST, instance=order)
        item_form = OrderItemForm(request.POST, instance=order.items.first())
        if order_form.is_valid() and item_form.is_valid():
            order = order_form.save()
            item = item_form.save(commit=False)
            item.order = order
            item.save()
            messages.success(request, 'Order updated successfully!')
            return redirect('customer_management:order_detail', pk=order.pk)
    else:
        order_form = OrderForm(instance=order)
        item_form = OrderItemForm(instance=order.items.first())
    
    return render(request, 'customer_management/order_form.html', {
        'order_form': order_form,
        'item_form': item_form,
        'title': 'Edit Order'
    })

@login_required
def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk, customer=request.user)
    
    if request.method == 'POST':
        order.delete()
        messages.success(request, 'Order deleted successfully!')
        return redirect('customer_management:order_list')
    
    return redirect('customer_management:order_list') 