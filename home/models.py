from django.conf import settings
import django.utils.timezone
from django.db import models
from users.models import User as us
from cryptography.fernet import Fernet
class Account(models.Model):
    accountID = models.AutoField(primary_key=True)
    cardNo = models.CharField(max_length=250, default="", blank=True)
    exp = models.DateField(default=django.utils.timezone.now)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)

class Movie(models.Model):
    title = models.CharField(primary_key=True, max_length=100)
    cast = models.CharField(max_length=100)
    synopsis = models.CharField(max_length=500)
    rating = models.CharField(max_length=5,blank=True)
    playing_now = models.BooleanField(default=False)  # if movie is playing now or coming soon
    trailer_picture = models.URLField(max_length=300)
    release_date = models.DateField(blank=True,default = None)
    genre = models.CharField(max_length=10,blank=True)
    trailer_video = models.URLField(max_length=250, blank=True)
    certificate = models.ForeignKey('MovieCategory', on_delete=models.CASCADE, default='G')
    director = models.CharField(max_length=100,blank=True,default='')
    producer = models.CharField(max_length=100,blank=True,default='')
    duration = models.CharField(max_length = 6,blank=True, null=True,default='03H00M')
class Ticket(models.Model):
    ticketID = models.AutoField(primary_key=True)
    seatNum = models.IntegerField(default=1)
    price = models.IntegerField(default=10)
    shownum = models.ForeignKey('Showtime', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    order = models.ForeignKey('Order', on_delete=models.CASCADE, blank=True, null=True)

class Showtime(models.Model):
    shownum = models.AutoField(primary_key=True)
    time = models.DateTimeField(blank=True, null=True,help_text="Format: YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ]")
    end_time = models.DateTimeField(blank=True, null=True,help_text="Format: YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ]")
    movieID = models.ForeignKey('Movie', on_delete=models.CASCADE, default='')
    screenID = models.ForeignKey('Screen', on_delete=models.CASCADE,default='')
    
    def createSeats(self):
        for i in range(1, 22):
            ticket = Ticket(seatNum=i, shownum=self)
            ticket.save()

class Screen(models.Model):
    SCREEN = (('A1','A1'),('A2','A2'),('A3','A3'),('A4','A4'),('A5','A5'))
    screen = models.CharField(primary_key=True, max_length=50,choices = SCREEN,default='A1')

class MovieCategory(models.Model):
    CATEGORY = (('G','General audience'),('M','Mature audience'),('R','Restricted audience'),('X','No one under 18'))
    category = models.CharField(primary_key=True, max_length=50,choices = CATEGORY,default='U')

    def __str__(self):
        return f"{self.category} - {self.get_category_display()}"
class Promotion(models.Model):
    promoID = models.AutoField(primary_key=True)
    promoCode = models.CharField(max_length=100,blank=True)
    amount = models.IntegerField(default=1)
    valid_thru = models.DateField(auto_now=False)

class CardEncr(models.Model):
    key = settings.ENCRYPT_KEY
    fernet = Fernet(key)

class Order(models.Model):
    orderID = models.AutoField(primary_key=True)
    total = models.IntegerField(default=0)
    numTickets = models.FloatField(default=0)
    userID = models.ForeignKey(us, on_delete=models.CASCADE, default=1)
    shownum = models.ForeignKey('Showtime', on_delete=models.CASCADE)
    accountID = models.ForeignKey('Account', on_delete=models.CASCADE, default=1, blank=True, null=True)