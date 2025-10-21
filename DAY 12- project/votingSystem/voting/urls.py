from django.urls import path
from . import views

urlpatterns = [
    path('', views.election_list, name='election_list'),
    path('register/', views.voter_registration, name='voter_registration'),
    path('election/<int:election_id>/', views.election_detail, name='election_detail'),
    path('election/<int:election_id>/vote/', views.vote, name='vote'),
    path('admin/create-election/', views.create_election, name='create_election'),
    path('admin/election/<int:election_id>/manage/', views.manage_election, name='manage_election'),
    path('admin/election/<int:election_id>/results/', views.election_results, name='election_results'),
]
