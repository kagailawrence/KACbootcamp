from django.urls import path
from . import views

urlpatterns = [
    path('', views.election_list, name='election_list'),
    path('register/', views.voter_registration, name='voter_registration'),
    path('election/<int:election_id>/', views.election_detail, name='election_detail'),
    path('election/<int:election_id>/vote/', views.vote, name='vote'),
    path('create-election/', views.create_election, name='create_election'),
    path('election/<int:election_id>/manage/', views.manage_election, name='manage_election'),
    path('election/<int:election_id>/results/', views.election_results, name='election_results'),
    # Dashboard URLs
    path('dashboard/admin/', views.AdminDashboardView.as_view(), name='admin_dashboard'),
    path('dashboard/auditor/', views.AuditorDashboardView.as_view(), name='auditor_dashboard'),
    path('dashboard/voter/', views.VoterDashboardView.as_view(), name='voter_dashboard'),
    path('auditor/export/csv/', views.export_audit_logs_csv, name='export_audit_csv'),
    path('auditor/export/pdf/', views.export_audit_logs_pdf, name='export_audit_pdf'),
    path('voter/verify/<uuid:ballot_id>/', views.verify_vote, name='verify_vote'),
    # Auth URLs
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
]
