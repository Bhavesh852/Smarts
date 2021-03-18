from django.contrib import admin

# Register your models here.
from .models import Contact, Complaints, Visitors

admin.site.register(Contact)
admin.site.register(Complaints)
admin.site.register(Visitors)