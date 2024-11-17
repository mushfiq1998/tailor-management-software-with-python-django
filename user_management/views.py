from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import (
    LoginView, PasswordChangeView, PasswordResetView, 
    PasswordResetConfirmView
)
from django.urls import reverse_lazy
from .forms import (
    UserRegistrationForm, UserProfileUpdateForm, 
    CustomerProfileForm, TailorProfileForm
)
from .models import CustomerProfile, TailorProfile

@login_required
def dashboard(request):
    return render(request, 'user_management/dashboard.html')

def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            
            # Create respective profile based on user type
            if user.user_type == 'CUSTOMER':
                CustomerProfile.objects.create(user=user)
            elif user.user_type == 'TAILOR':
                TailorProfile.objects.create(user=user)
            
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('dashboard')
    else:
        form = UserRegistrationForm()
    return render(request, 'user_management/register.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'user_management/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('dashboard')

@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserProfileUpdateForm(request.POST, instance=request.user)
        
        if request.user.user_type == 'CUSTOMER':
            profile_form = CustomerProfileForm(
                request.POST, 
                instance=request.user.customer_profile
            )
        else:
            profile_form = TailorProfileForm(
                request.POST, 
                instance=request.user.tailor_profile
            )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        user_form = UserProfileUpdateForm(instance=request.user)
        if request.user.user_type == 'CUSTOMER':
            profile_form = CustomerProfileForm(instance=request.user.customer_profile)
        else:
            profile_form = TailorProfileForm(instance=request.user.tailor_profile)

    return render(request, 'user_management/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'user_management/password_change.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        messages.success(self.request, 'Password changed successfully!')
        return super().form_valid(form)

class CustomPasswordResetView(PasswordResetView):
    template_name = 'user_management/password_reset.html'
    email_template_name = 'user_management/password_reset_email.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.success(self.request, 'Password reset email has been sent!')
        return super().form_valid(form)

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully!')
    return redirect('login')
