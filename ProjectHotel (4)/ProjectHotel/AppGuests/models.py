from django.db import models
from AppStaff.models import Room, Guest

class Booking(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('CHECKED_IN', 'Checked In'),
        ('CHECKED_OUT', 'Checked Out'),
        ('CANCELLED', 'Cancelled'),
    ]

    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True, blank=True)
    room_number = models.IntegerField(blank=True, null=True)
    check_in = models.DateField()
    check_out = models.DateField()
    number_of_guests = models.IntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')

    def __str__(self):
        return f'Booking for {self.guest.first_name} ({self.status})'

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(default='')
    subject = models.CharField(max_length=200)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    replied = models.BooleanField(default=False)
    reply = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Message from {self.name} - {self.subject}'