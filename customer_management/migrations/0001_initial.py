# Generated by Django 4.2.16 on 2024-11-17 16:19

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Measurement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_taken', models.DateTimeField(auto_now_add=True)),
                ('shoulder', models.DecimalField(decimal_places=2, max_digits=5)),
                ('chest', models.DecimalField(decimal_places=2, max_digits=5)),
                ('waist', models.DecimalField(decimal_places=2, max_digits=5)),
                ('hip', models.DecimalField(decimal_places=2, max_digits=5)),
                ('sleeve_length', models.DecimalField(decimal_places=2, max_digits=5)),
                ('inseam', models.DecimalField(decimal_places=2, max_digits=5)),
                ('outseam', models.DecimalField(decimal_places=2, max_digits=5)),
                ('thigh', models.DecimalField(decimal_places=2, max_digits=5)),
                ('knee', models.DecimalField(decimal_places=2, max_digits=5)),
                ('calf', models.DecimalField(decimal_places=2, max_digits=5)),
                ('notes', models.TextField(blank=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='measurements', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_date', models.DateTimeField(auto_now_add=True)),
                ('delivery_date', models.DateField()),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('CONFIRMED', 'Confirmed'), ('IN_PROGRESS', 'In Progress'), ('READY', 'Ready'), ('DELIVERED', 'Delivered'), ('CANCELLED', 'Cancelled')], default='PENDING', max_length=20)),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('advance_paid', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('special_instructions', models.TextField(blank=True)),
                ('is_rush_order', models.BooleanField(default=False)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL)),
                ('measurement', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='customer_management.measurement')),
                ('tailor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tailor_orders', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('garment_type', models.CharField(choices=[('SHIRT', 'Shirt'), ('PANTS', 'Pants'), ('SUIT', 'Suit'), ('DRESS', 'Dress'), ('SKIRT', 'Skirt'), ('OTHER', 'Other')], max_length=20)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='customer_management.order')),
            ],
        ),
        migrations.CreateModel(
            name='CustomerNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification_type', models.CharField(choices=[('ORDER_STATUS', 'Order Status Update'), ('PROMOTION', 'Promotional Message'), ('REMINDER', 'Reminder'), ('OTHER', 'Other')], max_length=20)),
                ('title', models.CharField(max_length=200)),
                ('message', models.TextField()),
                ('date_sent', models.DateTimeField(auto_now_add=True)),
                ('is_read', models.BooleanField(default=False)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CustomerFeedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('comment', models.TextField(blank=True)),
                ('date_submitted', models.DateTimeField(auto_now_add=True)),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='feedback', to='customer_management.order')),
            ],
        ),
    ]