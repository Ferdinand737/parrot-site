from django.shortcuts import render

def shop_page(request):
    return render(request,'payments/shop.html')