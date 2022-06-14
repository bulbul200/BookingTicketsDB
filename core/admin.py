from django.contrib import admin
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from .models import (
    CustomUser, Cars,Route,Schedules, Passengers, Sacco
)

"""register this custom user model with Django’s admin"""

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('email', 'name')
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("passwords don't match")
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):

    password = ReadOnlyPasswordHashField()
    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'name', 'is_active', 'is_admin')

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'name', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name',)}),
        ('Permissions', {'fields': ('is_admin',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2'),
        }),
    )


    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

# ---------------- End of Custom usercreation ------------->



class CarAdmin(admin.ModelAdmin):
    list_display = ('sacco', 'plate_name', 'plate_number', 'seats')


class RoutesAdmin(admin.ModelAdmin):
    list_display = ('departure', 'destination')

class SchedulessAdmin(admin.ModelAdmin):
    list_display = ('car', 'routes', 'date', 'time', 'price', 'full')


class PassengerAdmin(admin.ModelAdmin):
    list_display = ('schedules', 'seats', 'phone_number', 'confirm')

admin.site.register(CustomUser, UserAdmin)
admin.site.unregister(Group)
admin.site.register(Sacco)
admin.site.register(Cars, CarAdmin)
admin.site.register(Route, RoutesAdmin)
admin.site.register(Schedules, SchedulessAdmin)
admin.site.register(Passengers, PassengerAdmin)
