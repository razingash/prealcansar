
from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView, \
    PasswordResetDoneView
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, DetailView, ListView

from custom_user.forms import LoginCustomUserForm, RegisterCustomUserForm, ChangeCustomUserForm, \
    ChangeCustomUserPasswordForm, CustomPasswordResetForm, CustomPasswordResetConfirmForm
from custom_user.models import CustomUser
from utils.utils import DataMixin


# Create your views here.

class MainPageView(ListView, DataMixin):
    template_name = 'custom_user/main_page.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            mix = self.get_user_context(title='Main Page', user_uuid=self.request.user.uuid)
        else:
            mix = self.get_user_context(title='Main Page')
        return context | mix

    def get_queryset(self):
        pass


class RegistrationPageView(CreateView, DataMixin):
    form_class = RegisterCustomUserForm
    template_name = 'custom_user/registration.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        mix = self.get_user_context(title='Registration')
        return context | mix

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('custom_user:settings')


class LoginPageView(LoginView, DataMixin):
    template_name = 'custom_user/login.html'
    form_class = LoginCustomUserForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            mix = self.get_user_context(title='Login', user_uuid=self.request.user.uuid)
        else:
            mix = self.get_user_context(title='Login')
        return context | mix

    def get_success_url(self):
        user_uuid = self.request.user.uuid
        return reverse_lazy('custom_user:profile', kwargs={'profile_uuid': user_uuid})


class SettingsPasswordPage(LoginRequiredMixin, PasswordChangeView, DataMixin):
    template_name = 'custom_user/password_change.html'
    form_class = ChangeCustomUserPasswordForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            mix = self.get_user_context(title='password updating', user_uuid=self.request.user.uuid)
            return context | mix

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        user_uuid = self.request.user.uuid
        return reverse_lazy('custom_user:profile', kwargs={'profile_uuid': user_uuid})


class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'custom_user/password_reset.html'
    email_template_name = 'custom_user/password_reset_email.html'
    success_url = reverse_lazy('custom_user:password_reset_done')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('custom_user:main_page')
        return super().dispatch(request, *args, **kwargs)


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'custom_user/password_reset_done.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('custom_user:main_page')
        return super().dispatch(request, *args, **kwargs)


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomPasswordResetConfirmForm
    template_name = 'custom_user/password_reset_confirm.html'
    email_template_name = 'custom_user/password_reset_email.html'
    success_url = reverse_lazy('custom_user:password_reset_complete')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('custom_user:main_page')
        return super().dispatch(request, *args, **kwargs)


class RenewedLoginPageView(LoginView, DataMixin):
    template_name = 'custom_user/password_reset_complete.html'
    form_class = LoginCustomUserForm

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(reverse_lazy('custom_user:profile', kwargs={'profile_uuid': self.request.user.uuid}))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            mix = self.get_user_context(title='Login', user_uuid=self.request.user.uuid)
        else:
            mix = self.get_user_context(title='Login')
        return context | mix

    def get_success_url(self):
        user_uuid = self.request.user.uuid
        return reverse_lazy('custom_user:profile', kwargs={'profile_uuid': user_uuid})


class SettingsPageView(LoginRequiredMixin, FormView, DataMixin):
    template_name = 'custom_user/settings.html'
    form_class = ChangeCustomUserForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            mix = self.get_user_context(title='Settings', user_uuid=self.request.user.uuid)
            context.update(mix)
            return context | mix

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.request.user
        return kwargs

    def get_success_url(self):
        user_uuid = self.request.user.uuid
        return reverse_lazy('custom_user:profile', kwargs={'profile_uuid': user_uuid})


class ProfileView(DetailView, DataMixin):
    model = CustomUser
    template_name = 'custom_user/profile.html'
    context_object_name = 'user'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_object(self, queryset=None):
        profile_uuid = self.kwargs.get('profile_uuid')
        return get_object_or_404(CustomUser, uuid=profile_uuid)


def logout_user(request):
    logout(request)
    return redirect('custom_user:login')

