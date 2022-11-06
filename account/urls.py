from django.urls import path, include
from . import views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('login2/',views.user_login, name='login'),
    path('edit/', views.edit, name='edit'),
    path('add_report/', views.add_report, name='add_report'),
    path('view_reports/', login_required(views.ReportListView.as_view()), name='view_reports'),
    path('submit_done/', views.submit_done, name='submit_done'),
    path('delete/report/<report_id>',views.delete_report , name="delete view")






    
]
