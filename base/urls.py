from django.urls import path 
from .views import TaskList, TaskDetail, TaskCreate, TaskUpdate, DeleteView, CustomLoginView, RegisterPage
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # These paths are for user authentication.
    path('login/',CustomLoginView.as_view(), name='login'),  # login page
    path('logout/',LogoutView.as_view(next_page='login'), name='logout'),  # logout action, redirect to login page after logout
    path('register/', RegisterPage.as_view(), name='register'),  # register page

    # These paths are for task management.
    path('', TaskList.as_view(), name='tasks'),  # list of tasks
    path('task/<int:pk>/', TaskDetail.as_view(), name='task'),  # task detail page
    path('task-create/', TaskCreate.as_view(), name='task-create'),  # page to create new task
    path('task-update/<int:pk>/', TaskUpdate.as_view(), name='task-update'),  # page to update task
    path('task-delete/<int:pk>/', DeleteView.as_view(), name='task-delete'),  # action to delete task
]
