from django.db import models

class Guest(models.Model):
    first_name = models.CharField(max_length=100, default='')
    last_name = models.CharField(max_length=100, default='')
    email = models.EmailField(default='')
    phone_number = models.CharField(max_length=15, default='')
    id_front = models.ImageField(upload_to='guest_id_pictures/', null=True, blank=True)
    id_back = models.ImageField(upload_to='guest_id_pictures/', null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Room(models.Model):
    ROOM_TYPE_CHOICES = [
        ('STANDARD', 'Standard'),
        ('DELUXE', 'Deluxe'),
        ('SUITE', 'Suite'),
        ('FAMILY', 'Family'),
    ]
    room_type = models.CharField(max_length=20, choices=ROOM_TYPE_CHOICES, default='STANDARD')
    number_of_rooms = models.IntegerField(default=0)
    number_of_beds = models.IntegerField(default=1)
    rooms_available = models.IntegerField(default=0)
    price_per_night = models.FloatField(default=0.0)
    room_picture = models.ImageField(upload_to='room_pictures/', null=True, blank=True)
    description = models.TextField(default='', blank=True)

    def __str__(self):
        return f'{self.room_type} ({self.rooms_available}/{self.number_of_rooms} available)'