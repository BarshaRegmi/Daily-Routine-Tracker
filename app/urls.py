from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('plans/', views.plans, name='plans'),
    path('analytics/', views.analytics, name='analytics'),
    path('completed/', views.completed, name='completed'),
    path('add_plan/', views.add_plan, name='add_plan'),
    path('get_plans/', views.get_plans, name='get_plans'),
    path('update_completed/', views.update_completed, name='update_completed'),
    path('celery/', views.celery_test, name='celery'),

]
