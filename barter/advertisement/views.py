
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView, UpdateView

from advertisement.forms import AdvertisementForm, CreateCampaingForm, UpdateCampaingForm
from advertisement.models import Advertisement, Campaing
from services.advertisement.services import get_permission_for_updating_advertisement, \
    get_permission_for_updating_campaing
from utils.utils import DataMixin


class CampaingPageView(DetailView, DataMixin):
    model = Campaing
    template_name = 'advertisement/campaing.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_object(self, queryset=None):
        campaing_slug = self.kwargs.get('campaing_slug')
        return get_object_or_404(Campaing, campaing_slug=campaing_slug)


class CreateCampaingPageView(LoginRequiredMixin, FormView, DataMixin):
    form_class = CreateCampaingForm
    template_name = 'advertisement/create_campaing.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        return redirect(reverse_lazy('main_page'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            mix = self.get_user_context(title='New advertisement', user_uuid=self.request.user.uuid)
        else:
            mix = self.get_user_context(title='New advertisement')
        return context | mix

    def form_valid(self, form):
        form.instance.advertiser = self.request.user
        form = form.save()
        success_url = form.get_absolute_url()
        return HttpResponseRedirect(success_url)


class UpdateCampaingPageView(LoginRequiredMixin, UpdateView, DataMixin):
    form_class = UpdateCampaingForm
    template_name = 'advertisement/update_advertisement.html'

    def dispatch(self, request, *args, **kwargs):
        campaing_slug = self.kwargs.get('campaing_slug')
        if self.request.user.is_authenticated:
            permission = get_permission_for_updating_campaing(user=self.request.user, campaing_slug=campaing_slug)
            if permission is True:
                return super().dispatch(request, *args, **kwargs)
        return redirect(reverse_lazy('campaing', kwargs={'campaing_slug': campaing_slug}))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            mix = self.get_user_context(title='Update advertisement', user_uuid=self.request.user.uuid)
        else:
            mix = self.get_user_context(title='Update advertisement')
        return context | mix

    def get_object(self, queryset=None):
        campaing_slug = self.kwargs.get('campaing_slug')
        return get_object_or_404(Campaing, campaing_slug=campaing_slug)

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class AdvertisementPageView(DetailView, DataMixin):
    model = Advertisement
    template_name = 'advertisement/advertisement.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_object(self, queryset=None):
        title_slug = self.kwargs.get('title_slug')
        return get_object_or_404(Advertisement, title_slug=title_slug)


class CreateAdvertisementPageView(LoginRequiredMixin, FormView, DataMixin):
    form_class = AdvertisementForm
    template_name = 'advertisement/create_advertisement.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        return redirect(reverse_lazy('main_page'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            mix = self.get_user_context(title='New advertisement', user_uuid=self.request.user.uuid)
        else:
            mix = self.get_user_context(title='New advertisement')
        return context | mix

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.announcer = self.request.user
        form = form.save()
        success_url = form.get_absolute_url()
        return HttpResponseRedirect(success_url)


class UpdateAdvertisementPageView(LoginRequiredMixin, UpdateView, DataMixin):
    form_class = AdvertisementForm
    template_name = 'advertisement/update_advertisement.html'

    def dispatch(self, request, *args, **kwargs):
        title_slug = self.kwargs.get('title_slug')
        if self.request.user.is_authenticated:
            permission = get_permission_for_updating_advertisement(user=self.request.user, title_slug=title_slug)
            print(permission)
            if permission is True:
                return super().dispatch(request, *args, **kwargs)
        return redirect(reverse_lazy('advertisement', kwargs={'title_slug': title_slug}))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            mix = self.get_user_context(title='Update advertisement', user_uuid=self.request.user.uuid)
        else:
            mix = self.get_user_context(title='Update advertisement')
        return context | mix

    def get_object(self, queryset=None):
        title_slug = self.kwargs.get('title_slug')
        return get_object_or_404(Advertisement, title_slug=title_slug)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
