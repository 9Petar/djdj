from django.shortcuts import render, redirect
from .forms import GuestForm, BookingForm, ContactForm
from AppStaff.models import Room
from .models import ContactMessage

# Create your views here.
def index(request):
    return render(request, 'AppGuests/index.html')

def book(request):
    rooms = Room.objects.all()

    if request.method == 'POST':
        guest_form = GuestForm(request.POST, request.FILES)
        booking_form = BookingForm(request.POST)
        if guest_form.is_valid() and booking_form.is_valid():
            guest = guest_form.save()
            booking = booking_form.save(commit=False)
            booking.guest = guest
            room_type = booking_form.cleaned_data['room_type']
            for r in rooms:
                if r.room_type == room_type:
                    booking.room = r
                    break
            booking.status = 'PENDING'
            booking.save()
            return redirect('index')
    else:
        guest_form = GuestForm()
        booking_form = BookingForm()

    room_availability = {}
    for room in rooms:
        room_availability[room.room_type] = room.rooms_available > 0

    context = {}
    context['guest_form'] = guest_form
    context['booking_form'] = booking_form
    context['room_availability'] = room_availability
    return render(request, 'AppGuests/book.html', context)

def about(request):
    return render(request, 'AppGuests/about.html')

def contact(request):
    success = False

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            ContactMessage.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                subject=form.cleaned_data['subject'],
                message=form.cleaned_data['message']
            )
            form = ContactForm()
            success = True
    else:
        form = ContactForm()

    context = {}
    context['form'] = form
    if success:
        context['success'] = True
    return render(request, 'AppGuests/contact.html', context)

def rooms(request):
    rooms_list = Room.objects.all()
    context = {}
    context['rooms'] = rooms_list
    return render(request, 'AppGuests/rooms.html', context)

def custom_404(request, exception):
    return render(request, 'AppGuests/404.html', status=404)
