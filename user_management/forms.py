from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, PasswordResetForm
from .models import User, CustomerProfile, TailorProfile

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    user_type = forms.ChoiceField(
        choices=[('CUSTOMER', 'Customer'), ('TAILOR', 'Tailor')],  # Exclude ADMIN
        widget=forms.RadioSelect
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'user_type', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize form field labels and help texts
        self.fields['username'].help_text = 'Required. 150 characters or fewer.'
        self.fields['password1'].help_text = 'At least 8 characters.'
        self.fields['password2'].help_text = 'Enter the same password as before.'

class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'address']

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = CustomerProfile
        fields = ['gender', 'preferred_styles']

class TailorProfileForm(forms.ModelForm):
    class Meta:
        model = TailorProfile
        fields = ['experience_years', 'specialization', 'hourly_rate'] 