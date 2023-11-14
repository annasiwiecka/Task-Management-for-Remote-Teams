from django.urls import path 
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", views.index, name="index"),
    
    path("register/", views.register, name="register"),
    path("login/", views.loginPage, name="login"),
    path("logout", views.logoutPage, name="logout"),
    
    path("home", views.home, name="home"),
    
   path("profile/", views.profile, name="profile"),
   path("notification/", views.notification, name="notification"),
   path("team/<int:team_id>/", views.team, name="team_id"),
   
   path("my_task", views.my_task, name="my-task"),
   path('my_project', views.my_project, name='my_project'),
   path("Settings", views.settingsPage, name="settings"),

   path("create-team", views.create_team, name="create_team"),
   path("send_invitation", views.send_invitation, name="send_invitation"),
   path("notification/invitation/<int:invitation_id>/", views.invitation, name="invitation"),
   path("accept_invitation/<int:invitation_id>/", views.accept_invitation, name="accept_invitation"),
   path("decline_invitation/<int:invitation_id>/", views.decline_invitation, name="decline_invitation"),

    path('team_member/<int:team_member_id>/', views.team_member, name="team_member"),
    path('team_member/<int:team_member_id>/edit/', views.team_member_edit, name="team_member_edit"),
    path('team_member/<int:team_member_id>/delete', views.team_member_delete, name="team_member_delete"),
    path('team/<int:team_id>/create_project', views.create_project, name="create_project"),
    path('get_notification_count/', views.get_notification_count, name='get_notification_count'),
    path('team/<int:team_id>/team_members', views.list_members, name="list_of_members"),
    path('team/<int:team_id>/project_board', views.ProjectBoardListView.as_view(), name='project_board'),
    path("project/<int:project_id>/", views.project, name="project"),
    path('get_pending_project/<int:team_id>', views.get_pending_project, name='get_pending_project'),
    path('get_total_projects/<int:team_id>', views.get_total_projects, name='get_total_projects'),
    path('get_complete_projects/<int:team_id>', views.get_complete_projects, name='get_complete_projects'),
    path('get_pending_tasks/<int:team_id>', views.get_pending_tasks, name='get_pending_tasks'),
    path('get_total_tasks/<int:team_id>', views.get_total_tasks, name='get_total_tasks'),
    path('get_complete_tasks/<int:team_id>', views.get_complete_tasks, name='get_complete_tasks'),
    path('team/<int:team_id>/create_task/<int:project_id>/', views.create_task, name='create_task'),
    path('task/<int:task_id>/', views.task, name="task"),
    path('team/<int:team_id>/task_board', views.TaskBoardList.as_view(), name='task_board'),

] 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)