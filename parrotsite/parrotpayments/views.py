from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from .models import *
from datetime import datetime, timedelta
import requests
import os
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required(login_url="/?error=unauthorized") #will redirect to this url if user not logged in
def user_page(request, user_id):
  siteuser = SiteUser.objects.get(id=user_id)
  try:

    if request.user.id == int(request.path_info.split(r'/')[-2]):
        
        user = Users.objects.get(user_id=user_id)

        last_reset = user.last_char_reset
        next_reset = last_reset + timedelta(days=30)
        
        # Get the data for reload options
        reload_options = ReloadOptions.objects.all()
        context = {
          'user': user,
          'siteuser':siteuser,
          'next_reset': next_reset,
          'reload_options': reload_options,
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

def create_checkout_session_view(request, product_id):
  REDIRECT_DOMAIN = "http://127.0.0.1:8000"
  product = ReloadOptions.objects.get(id=product_id)
  checkout_session = stripe.checkout.Session.create(
    payment_method_types=['card'],
    line_items=[
        {
          'price_data': {
            'currency': 'usd',
            'unit_amount': product.price,
            'product_data': {
              'name': product.name,
              'description': product.description,
            },
          },
          'quantity': 1,
        },
    ],
    mode='payment',
    success_url=REDIRECT_DOMAIN + '/payments/success',
    cancel_url=REDIRECT_DOMAIN + '/payments/cancel',
  )
  return redirect(checkout_session.url, code=303)

def payment_success(request): return render(request, "paymentsuccess.html")
def payment_cancel(request): return render(request, "paymentcancel.html")