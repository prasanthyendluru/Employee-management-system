from django.contrib import admin
from .models import User, Task

# Register models in the admin panel
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_manager', 'is_employee')
    search_fields = ('username', 'email')

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'assigned_to', 'status')
    list_filter = ('status', 'assigned_to')
    search_fields = ('title', 'description')