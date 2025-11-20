from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Attempt)
admin.site.register(Customer)
admin.site.register(Customer_log)
admin.site.register(Room)
admin.site.register(Room_log)
admin.site.register(Room_check)