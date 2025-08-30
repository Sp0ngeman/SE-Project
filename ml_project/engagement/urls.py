from django.urls import path
from . import views

app_name = "engagement"

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('login/', views.login_view, name='login'),
    path('manual-import/', views.manual_import, name='manual_import'),
    path('auth-reminder/', views.auth_reminder, name='auth_reminder'),
    path('predict/<int:student_id>/', views.predict_for_student, name='predict'),
    path('student/<int:student_id>/', views.student_dashboard, name='student_dashboard'),
    path('export/csv/', views.export_csv, name='export_csv'),
    path('export/json/', views.export_json, name='export_json'),
]
