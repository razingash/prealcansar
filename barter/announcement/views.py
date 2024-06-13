
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView, UpdateView

from announcement.forms import CreateAnnouncementForm, UpdateAnnouncementForm
from announcement.models import Announcement
from services.announcement.services import get_permission_for_updating_announcement
from utils.utils import DataMixin
from django.utils.text import slugify

# Create your views here.


class AnnouncementPageView(DetailView, DataMixin):
    model = Announcement
    template_name = 'announcement/announcement.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_object(self, queryset=None):
        title_slug = self.kwargs.get('title_slug')
        return get_object_or_404(Announcement, title_slug=title_slug)


class CreateAnnouncementPageView(LoginRequiredMixin, FormView, DataMixin):
    form_class = CreateAnnouncementForm
    template_name = 'announcement/create_announcement.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        return redirect(reverse_lazy('main_page'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            mix = self.get_user_context(title='New announcement', user_uuid=self.request.user.uuid)
        else:
            mix = self.get_user_context(title='New announcement')
        return context | mix

    def form_valid(self, form):
        form.instance.announcer = self.request.user
        form.instance.title_slug = slugify(form.instance.title)
        form = form.save()
        success_url = form.get_absolute_url()
        return HttpResponseRedirect(success_url)


class UpdateAnnouncementPageView(LoginRequiredMixin, UpdateView, DataMixin):
    form_class = UpdateAnnouncementForm
    template_name = 'announcement/update_announcement.html'

    def dispatch(self, request, *args, **kwargs):
        title_slug = self.kwargs.get('title_slug')
        if self.request.user.is_authenticated:
            permission = get_permission_for_updating_announcement(user=self.request.user, title_slug=title_slug)
            print(permission)
            if permission is True:
                return super().dispatch(request, *args, **kwargs)
        return redirect(reverse_lazy('announcement', kwargs={'title_slug': title_slug}))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            mix = self.get_user_context(title='Update announcement', user_uuid=self.request.user.uuid)
        else:
            mix = self.get_user_context(title='Update announcement')
        return context | mix

    def get_object(self):
        title_slug = self.kwargs.get('title_slug')
        return get_object_or_404(Announcement, title_slug=title_slug)

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

