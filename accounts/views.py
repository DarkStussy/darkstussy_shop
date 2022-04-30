from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from accounts.forms import UserRegistrationForm, UserForm
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from accounts.token import account_activation_token
from cart.models import Cart


def login_user(request):
    error = ''
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("shop:home")
        else:
            error = 'Login or password is incorrect'

    return render(request, 'accounts/login_user.html', {'error': error})


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # save form in the memory not in database
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_active = False
            user.save()
            # to get the domain of the current site
            current_site = get_current_site(request)
            mail_subject = 'Activation link has been sent to your email id'
            message = render_to_string('accounts/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return render(request, 'accounts/register_confirm.html')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        Cart.objects.create(user=user)
        return render(request, 'accounts/register_done.html')
    else:
        return HttpResponse('Activation link is invalid!')


@login_required
def profile(request):
    if request.method == "POST":
        pass_form = PasswordChangeForm(user=request.user, data=request.POST)
        user_form = UserForm(request.POST, instance=request.user)
        if pass_form.is_valid():
            pass_form.save()
            update_session_auth_hash(request, pass_form.user)
            messages.success(request, 'Your password has been changed successfully!')
        elif user_form.is_valid():
            user_form.save()
            messages.success(request, 'Your profile has been saved successfully!')
        else:
            messages.error(request, 'Unable to complete request')
        return redirect("c_accounts:profile")
    user_form = UserForm(instance=request.user)
    pass_form = PasswordChangeForm(user=request.user)
    return render(request=request, template_name="accounts/profile.html", context={"user": request.user,
                                                                                   "user_form": user_form,
                                                                                   "pass_form": pass_form})
