from django.contrib.auth.backends import BaseBackend
from .models import SiteUsers
from django.contrib.auth.models import User

class DiscordAuthenticationBackend(BaseBackend):
  def authenticate(self, request, user) -> SiteUsers:
    find_user = SiteUsers.objects.filter(id=user['id'])
    if len(find_user) == 0:
      new_user = SiteUsers.objects.create_new_site_user(user)
      return new_user
    return find_user

  def get_user(self, user_id):
    try:
      return SiteUsers.objects.get(pk=user_id)
    except SiteUsers.DoesNotExist:
      return None