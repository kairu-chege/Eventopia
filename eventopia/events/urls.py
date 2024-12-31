from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('profile/', views.profile, name='profile'),
    path('events/', views.event_list, name='event_list'),
    path('events/<int:event_id>/', views.event_detail, name='event_detail'),
    path('events/create/', views.event_create, name='event_create'),
    path('events/<int:event_id>/update/', views.event_update, name='event_update'),
    path('events/<int:event_id>/delete/', views.event_delete, name='event_delete'),
    path('signup/', views.signup, name='signup'),  # Signup view
    path('login/', auth_views.LoginView.as_view(template_name='events/login.html'), name='login'),  # Login view
]
