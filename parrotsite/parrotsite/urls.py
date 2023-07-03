from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('discordlogin.urls')),
    path('shop/', include('payments.urls'))
]
