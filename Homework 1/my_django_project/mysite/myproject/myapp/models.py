from django.db import models
from django.utils import timezone

class Todo(models.Model):
    # The title of the task (e.g., "Buy Groceries")
    title = models.CharField(max_length=100)
    
    # Optional details about the task. null=True and blank=True allow this to be empty.
    description = models.TextField(null=True, blank=True)
    
    # The deadline. We use DateTimeField so you can set a specific time too.
    # null=True, blank=True means a due date is not required.
    due_date = models.DateTimeField(null=True, blank=True)
    
    # Tracks if the task is done. Default is False (not done).
    is_resolved = models.BooleanField(default=False)
    
    # Timestamps to track when the task was created and last updated.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # String representation: This is what you see in the admin panel or console.
    def __str__(self):
        status = "[x]" if self.is_resolved else "[ ]"
        return f"{status} {self.title}"
