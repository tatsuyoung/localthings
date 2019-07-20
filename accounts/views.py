from decouple import config
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.template.loader import get_template
from .forms import UserCreationForms, ContactForm, UserUpdateForm, ProfileUpdateForm


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForms(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('articles:list')
    else:
        form = UserCreationForms()
    return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('articles:list')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('articles:list')


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('accounts:profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'accounts/profile.html', context)


def Success(request):
    return render(request, 'accounts/success.html')


def Contact(request):
    Contact_Form = ContactForm
    if request.method == 'POST':
        form = Contact_Form(data=request.POST)

        if form.is_valid():
            contact_name = request.POST.get('contact_name')
            contact_email = request.POST.get('contact_email')
            contact_message = request.POST.get('message')
            template = get_template('accounts/contact_form.txt')
            context = {
                'contact_name': contact_name,
                'contact_email': contact_email,
                'contact_message': contact_message,
            }

            content = template.render(context)

            email = EmailMessage(
                'New contact form Localthings',
                content,
                'Local things' + '',
                [config('EMAIL_HOST_USER')],
                headers={'Reply To': contact_email}
            )

            email.send()
            return redirect('accounts:success')
    return render(request, 'accounts/contact.html', {'form': Contact_Form})
