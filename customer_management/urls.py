from django.urls import path
from . import views

app_name = 'customer_management'

urlpatterns = [
    # Measurement URLs
    path('measurements/', views.measurement_list, name='measurement_list'),
    path('measurements/create/', views.measurement_create, name='measurement_create'),
    path('measurements/<int:pk>/edit/', views.measurement_edit, name='measurement_edit'),
    path('measurements/<int:pk>/delete/', views.measurement_delete, name='measurement_delete'),
    
    # Order URLs
    path('orders/', views.order_list, name='order_list'),
    path('orders/create/', views.order_create, name='order_create'),
    path('orders/<int:pk>/', views.order_detail, name='order_detail'),
    path('orders/<int:pk>/edit/', views.order_edit, name='order_edit'),
    path('orders/<int:pk>/delete/', views.order_delete, name='order_delete'),
    
    # Feedback URLs
    path('orders/<int:order_pk>/feedback/', views.feedback_create, name='feedback_create'),
    
    # Notification URLs
    path('notifications/', views.notification_list, name='notification_list'),
] 