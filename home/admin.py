from django.contrib import admin

# Register your models here.
from home.models import ContactMessage

admin.site.register(ContactMessage)