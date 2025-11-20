from django.db import models
from django.utils import timezone
# Create your models here.
class Attempt(models.Model):
    username = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        local_time = timezone.localtime(self.timestamp)
        formatted_time = local_time.strftime("%Y-%m-%d %I:%M %p")
        return f"{self.username}    {'Success' if self.status else 'Failed'}    {formatted_time}"
    
    
class Customer_log(models.Model):
    cust_id=models.IntegerField()
    name=models.CharField(max_length=100)
    timestamp=models.DateTimeField(auto_now_add=True)
    action=models.CharField(max_length=50)
    

    def __str__(self):
        local_time = timezone.localtime(self.timestamp)
        formatted_time = local_time.strftime("%Y-%m-%d %I:%M %p")
        return f'{str(self.cust_id)}  -  {self.name}  -   {self.action}  on -  {formatted_time}'
    
class Room(models.Model):
    room_number=models.IntegerField(unique=True)
    type=models.CharField(max_length=50)
    price=models.IntegerField()
    available=models.BooleanField(default=True)

    def __str__(self):
        return f'Room no {self.room_number} - {self.type} - {"Available" if self.available else "Occupied"}'

class Room_log(models.Model):
    room_number=models.IntegerField()
    timestamp=models.DateTimeField(auto_now_add=True)
    action=models.CharField(max_length=50)

    def __str__(self):
        local_time = timezone.localtime(self.timestamp)
        formatted_time = local_time.strftime("%Y-%m-%d %I:%M %p")
        return f'Room {self.room_number}  -   {self.action}  on   {formatted_time}'

class Customer(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100)
    contact=models.IntegerField()
    address=models.TextField()
    id_proof=models.ImageField(upload_to='customer_id_proofs/', blank=False, null=False)

    def __str__(self):
        return f'{str(self.id)}   {self.name}'

class Room_check(models.Model):
    room_number=models.IntegerField()
    cust_id=models.IntegerField()
    check_in=models.DateTimeField()
    check_out=models.DateTimeField()


    def __str__(self):
        local_time_1 = timezone.localtime(self.check_in)
        local_time_2 = timezone.localtime(self.check_out)
        formatted_time_1 = local_time_1.strftime("%Y-%m-%d %I:%M %p")
        formatted_time_2 = local_time_2.strftime("%Y-%m-%d %I:%M %p")
        return f'Room {self.room_number} is occupied by Customer ID -{self.cust_id} from {formatted_time_1} to {formatted_time_2}'