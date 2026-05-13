from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Project, Task, Comment, Notification
#the dashboard view
@login_required
def dashboard(request):
    owned_projects = Project.objects.filter(owner=request.user)
    member_projects = Project.objects.filter(members=request.user)
    all_projects = (owned_projects | member_projects).distinct()
    unread_notifications = Notification.objects.filter(user=request.user, is_read=False).count()
    context = {
        'projects': all_projects,
        'unread_notifications': unread_notifications,
    }
    return render(request, 'projects/dashboard.html', context)
#create project view
@login_required
def create_project(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        if title:
            project = Project.objects.create(owner=request.user, title=title, description=description)
            messages.success(request, 'Project created!')
            return redirect('project_detail', pk=project.pk)
    return render(request, 'projects/create_project.html')

 # creating project detail view — the Kanban board:
@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    todo_tasks = project.tasks.filter(status='todo')
    inprogress_tasks = project.tasks.filter(status='inprogress')
    done_tasks = project.tasks.filter(status='done')
    members = project.members.all()
    total_tasks = project.tasks.count()
    done_count = done_tasks.count()
    progress = int((done_count / total_tasks) * 100) if total_tasks > 0 else 0
    context = {'project': project,'todo_tasks': todo_tasks,'inprogress_tasks': inprogress_tasks,'done_tasks': done_tasks,'members': members,'progress': progress,}
    return render(request, 'projects/project_detail.html', context)
#create task view
@login_required
def create_task(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        priority = request.POST.get('priority', 'medium')
        due_date = request.POST.get('due_date') or None
        assigned_to_id = request.POST.get('assigned_to') or None
        assigned_to = User.objects.filter(id=assigned_to_id).first() if assigned_to_id else None
        if title:
            task = Task.objects.create(project=project, title=title, description=description, priority=priority, due_date=due_date, assigned_to=assigned_to)
            if assigned_to and assigned_to != request.user:
                Notification.objects.create(user=assigned_to, message=f'{request.user.username} assigned you task: {task.title}')
            messages.success(request, 'Task created!')
            return redirect('project_detail', pk=pk)
    members = project.members.all()
    return render(request, 'projects/create_task.html', {'project': project, 'members': members})

#Task detail view:
@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    comments = task.comments.all().order_by('created_at')
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Comment.objects.create(task=task, author=request.user, content=content)
            if task.assigned_to and task.assigned_to != request.user:
                Notification.objects.create(user=task.assigned_to, message=f'{request.user.username} commented on task: {task.title}')
            return redirect('task_detail', pk=pk)
    return render(request, 'projects/task_detail.html', {'task': task, 'comments': comments})

#Update task status view:
@login_required
def update_task_status(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in ['todo', 'inprogress', 'done']:
            task.status = status
            task.save()
            messages.success(request, 'Task updated!')
        return redirect('project_detail', pk=task.project.pk)
    return redirect('dashboard')

#Notifications view:
@login_required
def notifications_view(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    notifications.update(is_read=True)
    return render(request, 'projects/notifications.html', {'notifications': notifications})