from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import TicketManager, RoleModel, AuthUser


@admin.register(RoleModel)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(AuthUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'role']
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('role',)}),
    )


@admin.register(TicketManager)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['ticketId', 'issue', 'clientId', 'role', 'status']
