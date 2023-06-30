from django.contrib.auth.backends import BaseBackend
from .models import SiteUser
from django.contrib.auth.models import User

class DiscordAuthenticationBackend(BaseBackend):
  def authenticate(self, request, user) -> SiteUser:
    find_user = SiteUser.objects.filter(id=user['id'])
    if len(find_user) == 0:
      print('User was not found. Saving...')
      new_user = SiteUser.objects.create_new_site_user(user)
      print(new_user)
      return new_user
    print('User was found. Returning...')
    return find_user

  def get_user(self, user_id):
    try:
      return SiteUser.objects.get(pk=user_id)
    except SiteUser.DoesNotExist:
      return None