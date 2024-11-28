from django.contrib import admin


# Register your models here.
# Derek was here!
from .models import Cake

from .models import Cake

class CakeAdmin(admin.ModelAdmin):
    # Add 'id' to the list of fields displayed in the admin list view
    list_display = ('id', 'name', 'price', 'description', 'created_at')
    # Add 'id' to the fields you can search or filter by if desired
    search_fields = ('id', 'name')
    list_filter = ('created_at',)

admin.site.register(Cake, CakeAdmin)
