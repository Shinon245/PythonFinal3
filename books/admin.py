from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from . import models

# Register your models here.


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed')
    search_fields = ('email',)
    list_filter = ('email',)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'dob', 'photo']
    filter_horizontal = ('favorites',)

class PokeAdmin(admin.ModelAdmin):
    list_display = ['name']

admin.site.register(models.Subscription, SubscriptionAdmin)
admin.site.register(models.Profile, ProfileAdmin)
admin.site.register(models.Pokemon, PokeAdmin)
