from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm
from .models import Profile
from .forms import TopUpForm
from .models import Transaction, Profile



def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your account has been created! You can now log in.")
            return redirect('users:login')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})


@login_required(login_url='users:login')
def user(request):
    profile = request.user.profile
    return render(request, 'users/user.html', {
        'user': request.user,
        'balance': profile.balance
    })

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', reverse("users:user"))
            return HttpResponseRedirect(next_url)
        else:
            messages.error(request, "Invalid Credentials.")
    return render(request, "users/login.html")

def logout_view(request):
    logout(request)
    messages.success(request, "Successfully logged out.")
    return redirect('users:login')

def user_view(request):
    profile = request.user.profile 
    return render(request, 'users/user.html', {
        'user': request.user,
        'balance': profile.balance
    })

@login_required
def top_up_view(request, user_id):
    profile = get_object_or_404(Profile, user_id=user_id)

    # Ensure the logged-in user is topping up their own account
    if request.user.id != user_id:
        messages.error(request, "You are not authorized to top up this account.")
        return redirect('users:user')

    if request.method == "POST":
        form = TopUpForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            profile.balance += amount
            profile.save()

            # Record the transaction
            Transaction.objects.create(users=request.user, amount=amount)

            messages.success(request, f"Your balance has been topped up by ${amount:.2f}.")
            return redirect('users:user')
        else:
            messages.error(request, "There was an error with your top-up. Please check the amount.")
    else:
        form = TopUpForm()

    context = {
        'form': form,
        'user_balance': profile.balance,
        'welcome_message': f"Welcome back, {request.user.first_name}!",
    }
    return render(request, 'users/top_up.html', context)

@login_required
def top_up_balance(request):
    profile = request.user.profile  

    if request.method == "POST":
        form = TopUpForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']  
            profile.balance += amount  
            profile.save()  
            
            # Rec the transaction
            Transaction.objects.create(user=request.user, amount=amount)
            
            # Notification
            messages.success(request, f"Your balance has been topped up by ${amount:.2f}.")
            return redirect('users:user')  # Redirect to user dashboard after success
        else:
            # jnvalid like alex turner
            messages.error(request, "There was an error with your top-up. Please check the amount.")
    else:
        form = TopUpForm()  

    return render(request, 'users/top_up.html', {'form': form})
