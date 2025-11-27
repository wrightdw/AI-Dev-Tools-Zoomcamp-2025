from django.shortcuts import render, redirect, get_object_or_404
from .models import Todo
from .forms import TodoForm

# 1. List all Todos
def todo_list(request):
    # Sort by resolved status (unresolved first) and then by due date
    todos = Todo.objects.all().order_by('is_resolved', 'due_date')
    return render(request, 'myapp/home.html', {'todos': todos})

# 2. Create a new Todo
def todo_create(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('todo_list')
    else:
        form = TodoForm()
    return render(request, 'myapp/todo_form.html', {'form': form})

# 3. Update an existing Todo
def todo_update(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            return redirect('todo_list')
    else:
        form = TodoForm(instance=todo)
    return render(request, 'myapp/todo_form.html', {'form': form})

# 4. Delete a Todo
def todo_delete(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    if request.method == 'POST':
        todo.delete()
        return redirect('todo_list')
    return render(request, 'myapp/todo_confirm_delete.html', {'todo': todo})

# 5. Quick Toggle (Mark as Resolved/Unresolved)
def todo_toggle_resolve(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    todo.is_resolved = not todo.is_resolved
    todo.save()
    return redirect('todo_list')