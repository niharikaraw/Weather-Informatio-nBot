from bot import views
from django.urls import path

from bot.views import home


urlpatterns = [
    path('5761837078:AAE8swqpRKGalpjwOaM4RKZXtDHIWn3-654', home),
    path('set_webhook/', views.set_webhook)
]