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
    privileges = models.CharField(max_length=255, default='normal_user')
    total_chars_used = models.IntegerField(default=0)
    monthly_char_limit = models.IntegerField(default=4000)
    monthly_chars_used = models.IntegerField(default=0)
    char_credit = models.IntegerField(default=0)
    last_char_reset = models.DateTimeField(default='1970-01-01 00:00:01')
    date_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'users'
        
    def add_characters(self, chars):
        self.char_credit += chars
        self.save()
        return
        
class ReloadOptions(models.Model):
    name = models.CharField(max_length=255, null=False)
    num_characters = models.IntegerField(null=False)
    price = models.IntegerField(default=0, null=False)
    description = models.CharField(max_length=255, default="", null=False)
    
    def __str__(self):
        return "Name: {self.name} | Characters: {self.characters} | Price: {self.get_display_price}"

    def get_display_price(self):
        return "{0:.2f}".format(self.price / 100)
