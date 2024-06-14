from advertisement.models import Advertisement, Campaing


def get_permission_for_updating_campaing(user, campaing_slug):
    permission = Campaing.objects.filter(advertiser=user, campaing_slug=campaing_slug)
    if permission.exists():
        return True
    return False

def get_permission_for_updating_advertisement(user, title_slug):
    permission = Advertisement.objects.select_related('campaing').filter(campaing__advertiser=user, title_slug=title_slug)
    if permission.exists():
        return True
    return False

