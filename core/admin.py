from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Role, User, Category, Transaction, Budget, Approval, Setting

admin.site.site_header = "Computer Science & AI Dept - Finance Dashboard Admin"
admin.site.site_title = "Finance Dashboard Admin"


class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {"fields": ("role",)}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {"fields": ("role",)}),
    )
    list_display = ("username", "email", "role", "is_staff")


admin.site.register(Role)
admin.site.register(User, UserAdmin)
admin.site.register(Category)
admin.site.register(Transaction)
admin.site.register(Budget)
admin.site.register(Approval)
admin.site.register(Setting)