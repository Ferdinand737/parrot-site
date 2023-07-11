from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from .models import *
import requests
import os
from datetime import datetime, timedelta


@login_required(login_url="/?error=unauthorized") #will redirect to this url if user not logged in
def user_page(request, user_id):
  siteuser = SiteUser.objects.get(id=user_id)

  try:

    if request.user.id == int(request.path_info.split(r'/')[-2]):
        
        user = Users.objects.get(user_id=user_id)

        last_reset = user.last_char_reset
        next_reset = last_reset + timedelta(days=30)
        context = {
          'user': user,
          'siteuser':siteuser,
          'next_reset': next_reset
        }
        
        return render(request, 'user.html', context)
    else:
        return render(request, '403.html', status=403)

  except Users.DoesNotExist:
    user = Users(
    user_id=siteuser.id,
    username=siteuser.discord_tag
    )
    user.save()



    return render(request, 'user.html', {'user': user,'siteuser':siteuser})
   
   
def index(request):
    return render(request, 'index.html')

def discord_login(request):
    return redirect(os.getenv('DISCORD_OAUTH'))

def login_redirect(request):
    code = request.GET.get('code')
    user = exchange_code(code)
    discord_user = authenticate(request, user=user)
    discord_user = list(discord_user).pop()
    login(request, discord_user)
    return redirect('user_page',user_id=discord_user.id)
  
def logout_view(request):
    user = request.user
    logout(request)
    print("User has been logged out")
    return redirect("/?status=logged_out")

   

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
