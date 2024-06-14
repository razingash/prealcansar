
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView, UpdateView

from announcement.forms import CreateAnnouncementForm, UpdateAnnouncementForm, AnnouncementImagesForm
from announcement.models import Announcement, AnnouncementMedia, AnnouncementImage
from services.announcement.services import get_permission_for_updating_announcement
from utils.utils import DataMixin


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
    template_name = 'announcement/create_announcement.html'
    form_class = CreateAnnouncementForm
    form_class_media = AnnouncementImagesForm

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            if self.request.method == 'GET':
                form_class_media = self.form_class_media(prefix='announcement_images_form')
                return self.render_to_response(self.get_context_data(form_class_media=form_class_media))
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
        print(0)
        form_media = self.form_class_media(self.request.POST, self.request.FILES, prefix='announcement_images_form')
        print(1)
        if form_media.is_valid() and form.is_valid():
            print(2)
            form.instance.announcer = self.request.user
            announcement = form.save()

            form_media.instance = announcement
            print(form_media.__dict__)
            media_files = form_media.cleaned_data['media']
            for media_file in media_files:
                announcement_media = AnnouncementMedia(media=media_file)
                announcement_media.save()
                announcement_image = AnnouncementImage(media=announcement_media, announcement=announcement)
                announcement_image.save()

                #announcement_media = AnnouncementMedia.objects.create(media=media_file)
                #announcement_image = AnnouncementImage.objects.create(media=announcement_media, announcement=announcement)

            success_url = announcement.get_absolute_url()
            return HttpResponseRedirect(success_url)
        else:
            return self.render_to_response(self.get_context_data(form_class=form, form_class_media=form_media))


class UpdateAnnouncementPageView(LoginRequiredMixin, UpdateView, DataMixin):
    form_class = UpdateAnnouncementForm
    template_name = 'announcement/update_announcement.html'

    def dispatch(self, request, *args, **kwargs):
        title_slug = self.kwargs.get('title_slug')
        if self.request.user.is_authenticated:
            permission = get_permission_for_updating_announcement(user=self.request.user, title_slug=title_slug)
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

    def get_object(self, queryset=None):
        title_slug = self.kwargs.get('title_slug')
        return get_object_or_404(Announcement, title_slug=title_slug)

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

