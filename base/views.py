from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Task

# Custom Login view for user authentication.


class CustomLoginView(LoginView):
    template_name = 'base/login.html'                   # login page template
    fields = '__all__'                                  # use all fields in form
    # if user is already authenticated, redirect
    redirect_authenticated_user = True

    # Method to define url to redirect after login successfully.
    def get_success_url(self):
        # reverse() executes immediatly, reverse_lazy() executes until the value is needed.
        return reverse_lazy('tasks')

# User registration view.


class RegisterPage(FormView):
    template_name = 'base/register.html'                # registration page template
    # use django's built-in user creation form
    form_class = UserCreationForm
    # redirect to tasks page after successful registration
    success_url = reverse_lazy('tasks')
    # redirect_authenticated_user = True   FormView does not support it, rewriete in get() below

    # Method to save user form and login user.
    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    # Method to redirect if user is already authenticated.
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)

# View to display list of tasks.


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    # context object name in the template
    context_object_name = 'tasks'

    # Method to filter tasks specific to the user.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(
                title__startswith=search_input)
        context['search_input'] = search_input
        return context

# View to display task details.


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html'

# View to create a new task.


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'complete']       # fields to use in form
    # fields = '__all__' # could list selected: fields = ['title']
    # redirect to tasks page after successful task creation
    success_url = reverse_lazy('tasks')

    # Method to set the user field in the task.
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)

# View to update a task.


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')

# View to delete a task.


class DeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
