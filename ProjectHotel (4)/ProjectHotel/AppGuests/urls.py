from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('book', views.book, name='book'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('sobe', views.rooms, name='rooms'),
]