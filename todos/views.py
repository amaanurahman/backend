from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from .models import Todo
from django.contrib.auth.decorators import login_required

# ===== REGISTER =====
def register_page(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'todos/register.html', {'form': form})

# ===== LOGIN =====
def login_page(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(request.GET.get('next') or '/')
    else:
        form = AuthenticationForm()
    return render(request, 'todos/login.html', {'form': form})

# ===== LOGOUT =====
def logout_user(request):
    logout(request)
    return redirect('/login/')

# ===== HOME =====
@login_required
def home(request):
    todos = Todo.objects.filter(user=request.user).order_by('complete', '-created_at')
    # incomplete first, completed at bottom
    return render(request, 'todos/home.html', {'todos': todos})

# ===== ADD TODO =====
@login_required
def add_todo(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        Todo.objects.create(user=request.user, title=title, description=description)
    return redirect('/')

# ===== EDIT TODO =====
@login_required
def edit_todo(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    if todo.complete:
        # Completed tasks cannot be edited
        return redirect('/')
    if request.method == 'POST':
        todo.title = request.POST.get('title')
        todo.description = request.POST.get('description')
        todo.save()
    return redirect('/')

# ===== DELETE TODO =====
@login_required
def delete_todo(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    todo.delete()
    return redirect('/')

# ===== TOGGLE COMPLETE =====
@login_required
def complete_todo(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    todo.complete = not todo.complete
    todo.save()
    return redirect('/')
