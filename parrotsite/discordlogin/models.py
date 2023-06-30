from django.db import models
from .managers import DiscordUserOAuth2Manager


# Create your models here.
class SiteUser(models.Model):
    objects = DiscordUserOAuth2Manager()

    id = models.BigIntegerField(primary_key=True)
    discord_tag = models.CharField(max_length=100)
    avatar = models.CharField(max_length=100)
    public_flags = models.IntegerField()
    flags = models.IntegerField()
    locale = models.CharField(max_length=100)
    mfa_enabled = models.BooleanField()
    last_login = models.DateTimeField(null=True)

    def is_authenticated(self, request):
        return True



class Users(models.Model):
    user_id = models.BigIntegerField(primary_key=True)
    username = models.CharField(max_length=255)
    privileges = models.CharField(max_length=255, blank=True, null=True)
    total_chars_used = models.IntegerField(blank=True, null=True)
    monthly_char_limit = models.IntegerField(blank=True, null=True)
    monthly_chars_used = models.IntegerField(blank=True, null=True)
    char_credit = models.IntegerField(blank=True, null=True)
    last_char_reset = models.DateTimeField(blank=True, null=True)
    date_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'

