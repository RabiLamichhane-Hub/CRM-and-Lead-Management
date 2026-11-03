from django.contrib import admin

# Register your models here.

from .models import (
    Customer,
    Project,
    SupportTicket,
    Lead,
    Inquiry,
)

admin.site.register(Customer)
admin.site.register(Project)
admin.site.register(SupportTicket)
admin.site.register(Lead)
admin.site.register(Inquiry)