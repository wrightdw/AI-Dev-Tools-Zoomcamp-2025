from django.contrib import admin
from .models import Todo

# This configuration class tells Django how to display the list of Todos
@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    # These fields will be shown as columns in the list view
    list_display = ('title', 'due_date', 'is_resolved', 'created_at')
    
    # You can click these fields to filter the list (e.g., show only resolved tasks)
    list_filter = ('is_resolved', 'due_date')
    
    # Adds a search bar to search by title or description
    search_fields = ('title', 'description')