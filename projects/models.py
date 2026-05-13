from django.db import models

from django.contrib.auth.models import User

class Project(models.Model):
    title=models.CharField(max_length=200)
    description =models.TextField(blank=True)
    owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name='owned_projects')
    members=models.ManyToManyField(User,related_name='memeber_projects',blank=True)
    created_at=models.DateTimeField(auto_now_add=True)

def str(self):
    return self.title

class Task(models.Model):
    STATUS_CHOICES=[('todo','To Do'),('inprogress','In Progress'),('done','Done'),]
    PRIORITY_CHOICES = [('low', 'Low'),('medium', 'Medium'),('high', 'High'),('urgent', 'Urgent'),]
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tasks')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

def str(self):
    return self.title

class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

def str(self):
    return f'{self.author.username}: {self.content[:30]}'

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

def str(self):
    return f'{self.user.username}: {self.message[:30]}'