from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import ResidencyProfile, UserProfile

# Register your models here.


# Define an inline admin class for the UserProfile model
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'User Profiles'


class ResidencyInline(admin.StackedInline):
    model = ResidencyProfile
    can_delete = False
    verbose_name_plural = 'Residency Profile'


# Extend the UserAdmin to include the UserProfileInline
class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline, ResidencyInline)


"""@admin.register(ResidencyProfile)
class ResidencyAdmin(admin.ModelAdmin):
    list_display = (
        'country',
        'district_city',
        'county',
        'parish',
        'village')
    list_filter = ('parish', 'village')
    search_fields = ('country', 'district_city', 'county')"""


# Registering models

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
