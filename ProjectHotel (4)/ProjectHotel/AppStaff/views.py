from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, user_passes_test
from AppGuests.models import Booking, ContactMessage
from django.contrib import messages

def is_staff(user):
    return user.is_staff

# Create your views here.
@login_required(login_url='/admin/login/')
@user_passes_test(is_staff, login_url='/admin/login/')
def dashboard(request):
    bookings = Booking.objects.order_by('check_in')
    context = {
        'bookings': bookings
    }
    return render(request, 'AppStaff/pending.html', context)


@login_required(login_url='/admin/login/')
@user_passes_test(is_staff, login_url='/admin/login/')
def approved_bookings(request):
    bookings = Booking.objects.order_by('check_in')
    context = {
        'bookings': bookings
    }
    return render(request, 'AppStaff/approved.html', context)


@login_required(login_url='/admin/login/')
@user_passes_test(is_staff, login_url='/admin/login/')
def active_bookings(request):
    bookings = Booking.objects.order_by('check_in')
    context = {
        'bookings': bookings
    }
    return render(request, 'AppStaff/active.html', context)


@login_required(login_url='/admin/login/')
@user_passes_test(is_staff, login_url='/admin/login/')
def booking_history(request):
    bookings = Booking.objects.order_by('check_in')
    context = {
        'bookings': bookings
    }
    return render(request, 'AppStaff/history.html', context)


@login_required(login_url='/admin/login/')
@user_passes_test(is_staff, login_url='/admin/login/')
def update_booking_status(request, booking_id):
    if request.method != 'POST':
        return redirect(request.META.get('HTTP_REFERER', 'staff_dashboard'))

    booking = Booking.objects.get(id=booking_id)
    new_status = request.POST.get('status', '')
    room_number_input = request.POST.get('room_number', '')

    if new_status != "":
        if new_status == 'CHECKED_IN':
            if room_number_input != "":
                is_room_taken = Booking.objects.filter(
                    status='CHECKED_IN',
                    room_number=room_number_input,
                ).exclude(id=booking.id).exists()

                if is_room_taken:
                    messages.error(request, 'Room already taken!')
                    return redirect(request.META.get('HTTP_REFERER', 'staff_dashboard'))

            booking.key_given = True

        booking.status = new_status

        if room_number_input != "":
            booking.room_number = room_number_input

        booking.save()

        if new_status == 'CHECKED_OUT' or new_status == 'CANCELLED':
            room_type = booking.room
            if room_type is not None:
                room_type.rooms_available = room_type.rooms_available + 1
                room_type.save()

    return redirect(request.META.get('HTTP_REFERER', 'staff_dashboard'))

@login_required(login_url='/admin/login/')
@user_passes_test(is_staff, login_url='/admin/login/')
def return_booking(request, booking_id):
    if request.method == 'POST':
        booking = Booking.objects.get(id=booking_id)
        room_type = booking.room
        if room_type.rooms_available > 0:
            booking.status = 'PENDING'
            booking.key_given = False
            room_type.rooms_available = room_type.rooms_available - 1
            booking.save()
            room_type.save()
        else:
            messages.error(request, 'No free rooms of that type!')
    return redirect(request.META.get('HTTP_REFERER', 'staff_dashboard'))

@login_required(login_url='/admin/login/')
@user_passes_test(is_staff, login_url='/admin/login/')
def messages_list(request):
    all_messages = ContactMessage.objects.all()
    messages_list = list(all_messages)
    messages_list.reverse()
    context = {
        'messages': messages_list
    }
    return render(request, 'AppStaff/messages.html', context)

def logout_view(request):
    logout(request)
    return redirect('/staff')
