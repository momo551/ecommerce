from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.http import JsonResponse
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm


# ---------------------------
# Register
# ---------------------------
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'redirect_url': '/accounts/profile/'})
            messages.success(request, f'Account created for {user.username}!')
            return redirect('accounts:profile')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                errors = {field: [str(err) for err in errs] for field, errs in form.errors.items()}
                return JsonResponse({'success': False, 'errors': errors})
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


# ---------------------------
# Login
# ---------------------------
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'redirect_url': '/products/'})
            return redirect('products:home')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                errors = {field: [str(err) for err in errs] for field, errs in form.errors.items()}
                return JsonResponse({'success': False, 'errors': errors})
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


# ---------------------------
# Profile
# ---------------------------
@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': 'Your account has been updated!'})
            messages.success(request, 'Your account has been updated!')
            return redirect('accounts:profile')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                errors = {}
                errors.update({f"user_{field}": [str(err) for err in errs] for field, errs in u_form.errors.items()})
                errors.update({f"profile_{field}": [str(err) for err in errs] for field, errs in p_form.errors.items()})
                return JsonResponse({'success': False, 'errors': errors})
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'accounts/profile.html', context)
