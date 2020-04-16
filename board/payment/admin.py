from django.contrib import admin
from payment.models import Contend

# Register your models here.

class ContendAdmin(admin.ModelAdmin):
    list_display = ('owner', 'rent',)
    list_filter = ('owner', 'rent',)

    search_fields = ('owner', 'rent',) 

    actions = []

admin.site.register(Contend,ContendAdmin)