from django.test import TestCase
from django.urls import reverse
from .models import Todo

class TodoModelTest(TestCase):
    def test_string_representation(self):
        """Test that the model prints nicely (e.g., '[ ] Title')"""
        todo = Todo.objects.create(title="Test Task")
        self.assertEqual(str(todo), "[ ] Test Task")
        
        todo.is_resolved = True
        self.assertEqual(str(todo), "[x] Test Task")

    def test_defaults(self):
        """Test that is_resolved defaults to False"""
        todo = Todo.objects.create(title="Default Check")
        self.assertFalse(todo.is_resolved)


class TodoViewTest(TestCase):
    def setUp(self):
        """Create a sample task before each test runs"""
        self.todo = Todo.objects.create(title="Sample Task", description="Test Desc")

    def test_todo_list_view(self):
        """Homepage should load and show our task"""
        response = self.client.get(reverse('todo_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sample Task")
        self.assertTemplateUsed(response, 'myapp/home.html')

    def test_todo_create_view(self):
        """Submitting the form should create a new task"""
        response = self.client.post(reverse('todo_create'), {
            'title': 'New Created Task',
            'description': 'Created via test',
            'is_resolved': False
        })
        # Should redirect to list after success
        self.assertEqual(response.status_code, 302) 
        self.assertEqual(Todo.objects.count(), 2) # 1 from setUp + 1 new one

    def test_todo_update_view(self):
        """Editing a task should save changes"""
        response = self.client.post(reverse('todo_update', args=[self.todo.pk]), {
            'title': 'Updated Title',
            'description': 'Updated Desc',
            'is_resolved': True
        })
        self.assertEqual(response.status_code, 302)
        
        # Reload from DB to check changes
        self.todo.refresh_from_db()
        self.assertEqual(self.todo.title, 'Updated Title')
        self.assertTrue(self.todo.is_resolved)

    def test_todo_delete_view(self):
        """Deleting a task should remove it from DB"""
        response = self.client.post(reverse('todo_delete', args=[self.todo.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Todo.objects.count(), 0)

    def test_todo_toggle_view(self):
        """Toggling should flip the boolean status"""
        # Initially False (from setUp default)
        self.assertFalse(self.todo.is_resolved)
        
        # Hit the toggle URL
        self.client.get(reverse('todo_toggle_resolve', args=[self.todo.pk]))
        
        # Check it flipped to True
        self.todo.refresh_from_db()
        self.assertTrue(self.todo.is_resolved)