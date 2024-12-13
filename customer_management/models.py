from django.db import models
from user_management.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Measurement(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, 
                                 related_name='measurements')
    date_taken = models.DateTimeField(auto_now_add=True)
    
    # Upper body measurements
    shoulder = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        help_text="Measure across the back from shoulder point to shoulder point"
    )
    chest = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        help_text="Measure around the fullest part of the chest, keeping the tape parallel to the floor"
    )
    waist = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        help_text="Measure around the natural waistline, the narrowest part of the torso"
    )
    hip = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        help_text="Measure around the fullest part of the hips, keeping the tape parallel to the floor"
    )
    sleeve_length = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        help_text="Measure from shoulder point to wrist with arm slightly bent"
    )
    
    # Lower body measurements
    inseam = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        help_text="Measure from the crotch seam to the desired length of the pants"
    )
    outseam = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        help_text="Measure from the waist to the desired length of the pants along the outside of the leg"
    )
    thigh = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        help_text="Measure around the fullest part of the thigh"
    )
    knee = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        help_text="Measure around the knee with leg slightly bent"
    )
    calf = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        help_text="Measure around the fullest part of the calf muscle"
    )
    
    notes = models.TextField(
        blank=True,
        help_text="Any additional notes about the measurements or specific requirements"
    )

    def __str__(self):
        return f"{self.customer.username}'s measurements - {self.date_taken.strftime('%Y-%m-%d')}"

class Order(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('IN_PROGRESS', 'In Progress'),
        ('READY', 'Ready'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    )
    
    customer = models.ForeignKey(User, on_delete=models.CASCADE, 
                                 related_name='orders')
    tailor = models.ForeignKey(User, on_delete=models.CASCADE, 
                              related_name='tailor_orders')
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, 
                             default='PENDING')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    advance_paid = models.DecimalField(max_digits=10, decimal_places=2, 
                                       default=0)
    measurement = models.ForeignKey(Measurement, on_delete=models.PROTECT)
    
    special_instructions = models.TextField(blank=True)
    is_rush_order = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Order #{self.id} - {self.customer.username}"

class OrderItem(models.Model):
    GARMENT_CHOICES = (
        ('ALL', 'All'),
        ('PAIJAMA', 'Paijama'),
        ('PANJABI', 'Panjabi'),
        ('PANJABI_SET', 'Panjabi Set'),
        ('JUBBA', 'Jubba'),

        ('SHIRT', 'Shirt'),
        ('PANTS', 'Pants'),
        ('SUIT', 'Suit'),
        ('COAT', 'Coat'),
        ('SHERWANI', 'Sherwani'),

        ('SKIRT', 'Skirt'),
        ('THREES_PIECE', '3 Piece'),
        ('BLOUSE', 'Blouse'),
        ('SHORTS', 'Shorts'),
        ('JEANS', 'Jeans'),
        ('TROUSERS', 'Trousers'),
        ('OTHER', 'Other'),
    )
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE, 
                              related_name='items')
    garment_type = models.CharField(max_length=20, choices=GARMENT_CHOICES)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    
    def __str__(self):
        return f"{self.garment_type} - Order #{self.order.id}"

class CustomerFeedback(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, 
                                 related_name='feedback')
    rating = models.IntegerField(validators=[MinValueValidator(1), 
                                             MaxValueValidator(5)])
    comment = models.TextField(blank=True)
    date_submitted = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Feedback for Order #{self.order.id}"

class CustomerNotification(models.Model):
    NOTIFICATION_TYPES = (
        ('ORDER_STATUS', 'Order Status Update'),
        ('PROMOTION', 'Promotional Message'),
        ('REMINDER', 'Reminder'),
        ('OTHER', 'Other'),
    )
    
    customer = models.ForeignKey(User, on_delete=models.CASCADE, 
                                 related_name='notifications')
    notification_type = models.CharField(max_length=20, 
                                         choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.notification_type} - {self.customer.username}" 