from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, JsonResponse
from .models import *
import requests
import os

def user_page(request, user_id):
  try:
    siteuser = SiteUser.objects.get(id=user_id)
    user = Users.objects.get(user_id=user_id)
    return render(request, 'discordlogin/user.html', {'user': user,'siteuser':siteuser})
  except Users.DoesNotExist:
    return HttpResponse('User not found', status=404)
   
   
def index(request):
    return render(request, 'discordlogin/index.html')

def discord_login(request):
    return redirect(os.getenv('DISCORD_OAUTH'))

def login_redirect(request):
    code = request.GET.get('code')
    user = exchange_code(code)
    discord_user = authenticate(request, user=user)
    discord_user = list(discord_user).pop()
    login(request, discord_user)
    return redirect('user_page',user_id=discord_user.id)

   

def exchange_code(code: str):

  data = {
    "client_id": os.getenv('CLIENT_ID'),
    "client_secret": os.getenv('CLIENT_SECRET'),
    "grant_type": "authorization_code",
    "code": code,
    "redirect_uri": os.getenv('DISCORD_REDIRECT_URI'),
    "scope": "identify"
  }
  headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
  }
  response = requests.post("https://discord.com/api/oauth2/token", data=data, headers=headers)
  print(response)
  credentials = response.json()
  access_token = credentials['access_token']
  response = requests.get("https://discord.com/api/v6/users/@me", headers={
    'Authorization': 'Bearer %s' % access_token
  })
  user = response.json()
  return user
