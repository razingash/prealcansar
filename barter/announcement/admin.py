from django.contrib import admin

from announcement.models import AnnouncementTag, Announcement, Tag

# Register your models here.

admin.site.register(Announcement)
admin.site.register(Tag)
admin.site.register(AnnouncementTag)
