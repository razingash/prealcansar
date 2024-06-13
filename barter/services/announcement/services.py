from announcement.models import Announcement


def get_permission_for_updating_announcement(user, title_slug):
    permission = Announcement.objects.filter(announcer=user, title_slug=title_slug)
    if permission.exists():
        return True
    return False
