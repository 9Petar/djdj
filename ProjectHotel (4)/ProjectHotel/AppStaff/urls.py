from django.urls import path
from . import views
from . import email

urlpatterns = [
    path('', views.dashboard, name="staff_dashboard"),
    path('approved/', views.approved_bookings, name="approved_bookings"),
    path('active/', views.active_bookings, name="active_bookings"),
    path('history/', views.booking_history, name="booking_history"),
    path('update_status/<int:booking_id>/', views.update_booking_status, name="update_booking_status"),
    path('return_booking/<int:booking_id>/', views.return_booking, name="return_booking"),
    path('messages/', views.messages_list, name="staff_messages"),
    path('reply-message/', email.reply_message, name="reply_message"),
    path('logout/', views.logout_view, name="logout"),
]

