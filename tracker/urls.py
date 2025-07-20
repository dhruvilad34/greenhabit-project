from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('goals/', views.goal_list, name='goal_list'),
    path('submit/', views.submit_goal, name='submit_goal'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('history/', views.visit_history, name='visit_history'),
    path('about/', views.about, name='about'),
    path('like/<int:goal_id>/', views.like_goal, name='like_goal'),
    path('comment/<int:goal_id>/', views.add_comment, name='add_comment'),
path('mygoals/', views.my_goals, name='my_goals'),
path('goal/edit/<int:goal_id>/', views.edit_goal, name='edit_goal'),
path('goal/delete/<int:goal_id>/', views.delete_goal, name='delete_goal'),
path('blog/<int:pk>/', views.blog_detail, name='blog_detail'),

]


