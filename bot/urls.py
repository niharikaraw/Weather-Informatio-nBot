from bot import views
from django.urls import path

from bot.views import home


urlpatterns = [
    path('5638078202:AAFWEkY1BWBssZiXm9RCWcqUYZiBN4CZV_M', home),
    path('set_webhook/', views.set_webhook)
]