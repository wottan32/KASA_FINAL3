import requests
import json
from django.utils import translation
from django.http import HttpResponse
from django.shortcuts import redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView
from django.views.generic import FormView, DetailView, UpdateView  # View
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from . import forms, models, mixins
from users.utils import get_token_and_profile
from users.exceptions import GithubException


class LoginView(mixins.LoggedOutOnlyView, FormView):
    template_name = "users/login.html"
    form_class = forms.LoginForm

    def form_valid(self, form):
        # post
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)

    def get_success_url(self):
        next_arg = self.request.GET.get("next")
        if next_arg is not None:
            return next_arg
        else:
            return reverse("core:home")


def log_out(request):
    messages.info(request, f"See you later")
    logout(request)
    return redirect(reverse("core:home"))


class SignUpView(mixins.LoggedOutOnlyView, FormView):
    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        user.verify_email()
        return super().form_valid(form)


def complete_verification(request, key):
    try:
        user = models.User.objects.get(email_secret=key)
        user.email_verified = True
        user.email_secret = ""
        user.is_active = True
        user.save()
        # print("email verificado")
    except models.User.DoesNotExist:
        # print("usuario no existe")
        pass
    return redirect(reverse("core:home"))


def github_login(request):
    client_id = "df6a5412a07f33314d1d"
    redirect_uri = "http://127.0.0.1:8000/users/login/github/callback"
    return redirect(
        f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=read:user"
    )

def github_callback(request):
    client_id = "df6a5412a07f33314d1d"
    client_secret = "574012c80fc95a3f23b5ebaf442e82aa5c896995"
    code = request.GET.get("code", None)

    try:
        token_json, profile_json = get_token_and_profile(client_id, client_secret, code)
        username = profile_json.get("login", None)
        if username is not None:
            name = profile_json.get("name")
            email = profile_json.get("email")
            bio = profile_json.get("bio")
            user = models.User.objects.get_or_create(
                email=email, defaults={
                    'first_name': name,
                    'username': email,
                    'bio': bio,
                    'login_method': models.User.LOGIN_GITHUB,
                    'email_verified': True,
                }
            )[0]
            user.set_unusable_password()
            user.save()
            # login(request, user)
            login(request, user, backend='social_core.backends.github.GithubOAuth2')
            messages.success(request, f"Welcome back {user.first_name}")
            return redirect(reverse("core:home"))
        else:
            raise GithubException("Can't get your profile")
    except GithubException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))


class UserProfileView(DetailView):
    model = models.User
    context_object_name = "user_obj"


class UpdateProfileView(mixins.LoggedInOnlyView, SuccessMessageMixin, UpdateView):
    model = models.User
    template_name = "users/update-profile.html"
    fields = (
        "first_name",
        "last_name",
        "gender",
        "bio",
        "birthdate",
        "language",
        "currency",
    )
    success_message = "Profile Updated"

    def get_object(self, queryset=None):
        return self.request.user

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["first_name"].widget.attrs = {"placeholder": "First name"}
        form.fields["last_name"].widget.attrs = {"placeholder": "Last name"}
        form.fields["bio"].widget.attrs = {"placeholder": "Bio \n (ex. I love traveling)"}
        form.fields["birthdate"].widget.attrs = {"placeholder": "Birthdate \n (ex. 1990-01-01)"}
        form.fields["first_name"].widget.attrs = {"placeholder": "First name"}

        # photo
        return form


class UpdatePasswordView(
    mixins.LoggedInOnlyView,
    mixins.EmailLoginOnlyView,
    SuccessMessageMixin,
    PasswordChangeView,
):
    template_name = "users/update-password.html"
    success_message = "Password Updated"

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["old_password"].widget.attrs = {"placeholder": "Current password"}
        form.fields["new_password1"].widget.attrs = {"placeholder": "New password"}
        form.fields["new_password2"].widget.attrs = {
            "placeholder": "Confirm new password"
        }
        return form

    def get_success_url(self):
        return self.request.user.get_absolute_url()


@login_required
def switch_hosting(request):
    try:
        del request.session["is_hosting"]
    except KeyError:
        request.session["is_hosting"] = True
    return redirect(reverse("core:home"))


def switch_language(request):
    lang = request.GET.get("lang", None)
    if lang is not None:
        request.session[translation.LANGUAGE_SESSION_KEY] = lang  # LANGUAGE_SESSION_KEY
    return HttpResponse(status=200)
