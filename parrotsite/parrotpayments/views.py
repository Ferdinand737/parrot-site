from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from .models import *
from .helpers import fulfill_order
from datetime import datetime, timedelta
import requests
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required(login_url="/?error=unauthorized") #will redirect to this url if user not logged in
def user_page(request, user_id, purchase_status=None):
  siteuser = SiteUsers.objects.get(id=user_id)
  try:

    if request.user.id == int(request.path_info.split(r'/')[-2]):
        
        user = Users.objects.get(user_id=user_id)

        last_reset = user.last_char_reset
        next_reset = last_reset + timedelta(days=30)
        
        # Get the data for reload options
        products = Products.objects.all()
        transactions = Transactions.objects.filter(user_id=user_id)        
        context = {
          'user': user,
          'siteuser':siteuser,
          'next_reset': next_reset,
          'products': products,
          'transactions': transactions,
          'purchase_status': purchase_status,
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
  print(request.user)
  if request.user.id:
    return redirect("/user_page/%s" % request.user.id)
  return render(request, 'index.html')

def discord_login(request):
    return redirect(settings.DISCORD_OAUTH)

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
    return redirect("/?status=logged_out")
   
def exchange_code(code: str):
  data = {
    "client_id": settings.DISCORD_CLIENT_ID,
    "client_secret": settings.DISCORD_CLIENT_SECRET,
    "grant_type": "authorization_code",
    "code": code,
    "redirect_uri": settings.DISCORD_REDIRECT_URI,
    "scope": "identify"
  }
  headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
  }
  response = requests.post("https://discord.com/api/oauth2/token", data=data, headers=headers)
  credentials = response.json()
  print(response.content)
  access_token = credentials['access_token']
  response = requests.get("https://discord.com/api/v6/users/@me", headers={
    'Authorization': 'Bearer %s' % access_token
  })
  user = response.json()
  return user

def create_checkout_session_view(request, product_id):
  REDIRECT_DOMAIN = settings.STRIPE_REDIRECT_DOMAIN + request.user.id
  product = Products.objects.get(id=product_id)
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
    metadata={
      'product_id': product.id,
      'user_id': request.user.id,
      },
    mode='payment',
    success_url=f"{REDIRECT_DOMAIN}/success",
    cancel_url=f"{REDIRECT_DOMAIN}/cancelled",
  )
  return redirect(checkout_session.url, code=303)

@csrf_exempt
def stripe_webhook(request):
  payload = request.body
  sig_header = request.META['HTTP_STRIPE_SIGNATURE']
  event = None

  try:
    event = stripe.Webhook.construct_event(
      payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
    )
  except ValueError as e:
    # Invalid payload
    return HttpResponse(status=400)
  except stripe.error.SignatureVerificationError as e:
    # Invalid signature
    return HttpResponse(status=400)

  # Handle the checkout.session.completed event
  if event['type'] == 'checkout.session.completed':
    # Retrieve the session. If you require line items in the response, you may include them by expanding line_items.
    session = stripe.checkout.Session.retrieve(
      event['data']['object']['id'],
      expand=['line_items'],
    )
    
    fulfill_order(session)
  # Passed signature verification
  return HttpResponse(status=200)