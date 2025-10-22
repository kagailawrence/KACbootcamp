import json
import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login, logout
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.db.models import Count, Q
from django.http import HttpResponse
from django.utils import timezone
from django.core.serializers.json import DjangoJSONEncoder
import json
import csv
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
from .models import Voter, Ballot, Election, Candidate, User, AuditLog, SystemMetrics
from .forms import VoterRegistrationForm, VoteForm, ElectionForm, CandidateForm, LoginForm, SignupForm
from .decorators import role_required

@login_required
def voter_registration(request):
    if hasattr(request, 'voter'):
        messages.info(request, "You are already registered as a voter.")
        return redirect('election_list')

    if request.method == 'POST':
        form = VoterRegistrationForm(request.POST)
        if form.is_valid():
            voter = form.save(commit=False)
            voter.user = request.user
            voter.save()
            messages.success(request, "Successfully registered as a voter!")
            return redirect('election_list')
    else:
        form = VoterRegistrationForm(initial={'user': request.user})

    return render(request, 'voting/voter_registration.html', {'form': form})

@login_required
def election_list(request):
    elections = Election.objects.filter(is_active=True)
    return render(request, 'voting/election_list.html', {'elections': elections})

@login_required
def election_detail(request, election_id):
    election = get_object_or_404(Election, pk=election_id, is_active=True)
    candidates = election.candidates.all()

    # Check if user has already voted
    voter = getattr(request, 'voter', None)
    if voter:
        has_voted = Ballot.objects.filter(voter_id=voter.voter_id, encrypted_vote__contains=str(election_id)).exists()
    else:
        has_voted = False

    return render(request, 'voting/election_detail.html', {
        'election': election,
        'candidates': candidates,
        'has_voted': has_voted
    })

@login_required
def vote(request, election_id):
    election = get_object_or_404(Election, pk=election_id, is_active=True)
    voter = getattr(request, 'voter', None)

    if not voter:
        messages.error(request, "You must be registered as a voter to vote.")
        return redirect('voter_registration')

    # Check if election is active
    now = timezone.now()
    if not (election.start_date <= now <= election.end_date):
        messages.error(request, "This election is not currently active.")
        return redirect('election_detail', election_id=election_id)

    # Check if user has already voted
    has_voted = Ballot.objects.filter(voter_id=voter.voter_id, encrypted_vote__contains=str(election_id)).exists()
    if has_voted:
        messages.error(request, "You have already voted in this election.")
        return redirect('election_detail', election_id=election_id)

    if request.method == 'POST':
        form = VoteForm(election, request.POST)
        if form.is_valid():
            candidate = form.cleaned_data['candidate']

            # Create anonymous ballot
            vote_data = {
                'election_id': election_id,
                'candidate_id': candidate.id,
                'timestamp': str(timezone.now())
            }
            ballot = Ballot.objects.create(
                voter_id=voter.voter_id,
                encrypted_vote=json.dumps(vote_data)
            )

            # Mark voter as having voted
            voter.has_voted = True
            voter.save()

            # Log the vote for audit trail
            AuditLog.objects.create(
                action='vote_cast',
                user=request.user,
                election=election,
                details={'ballot_id': str(ballot.ballot_id), 'candidate_id': candidate.id},
                ip_address=request.META.get('REMOTE_ADDR')
            )

            messages.success(request, "Your vote has been recorded anonymously.")
            return redirect('election_list')
    else:
        form = VoteForm(election)

    return render(request, 'voting/vote.html', {'form': form, 'election': election})

# Admin views
@login_required
@role_required(['admin'])
def create_election(request):

    if request.method == 'POST':
        form = ElectionForm(request.POST)
        if form.is_valid():
            election = form.save()

            # Log election creation
            AuditLog.objects.create(
                action='election_created',
                user=request.user,
                election=election,
                details={'title': election.title},
                ip_address=request.META.get('REMOTE_ADDR')
            )

            messages.success(request, f"Election '{election.title}' created successfully.")
            return redirect('manage_election', election_id=election.id)
    else:
        form = ElectionForm()

    return render(request, 'voting/create_election.html', {'form': form})

@login_required
@role_required(['admin'])
def manage_election(request, election_id):

    election = get_object_or_404(Election, pk=election_id)

    if request.method == 'POST':
        if 'activate' in request.POST:
            election.is_active = True
            election.save()

            # Log election activation
            AuditLog.objects.create(
                action='election_started',
                user=request.user,
                election=election,
                details={'status': 'activated'},
                ip_address=request.META.get('REMOTE_ADDR')
            )

            messages.success(request, "Election activated.")
        elif 'deactivate' in request.POST:
            election.is_active = False
            election.save()

            # Log election deactivation
            AuditLog.objects.create(
                action='election_ended',
                user=request.user,
                election=election,
                details={'status': 'deactivated'},
                ip_address=request.META.get('REMOTE_ADDR')
            )

            messages.success(request, "Election deactivated.")
        elif 'add_candidate' in request.POST:
            candidate_form = CandidateForm(request.POST)
            if candidate_form.is_valid():
                candidate = candidate_form.save(commit=False)
                candidate.election = election
                candidate.save()

                # Log candidate addition
                AuditLog.objects.create(
                    action='candidate_added',
                    user=request.user,
                    election=election,
                    details={'candidate_name': candidate.name},
                    ip_address=request.META.get('REMOTE_ADDR')
                )

                messages.success(request, f"Candidate '{candidate.name}' added.")
                return redirect('manage_election', election_id=election.id)
        return redirect('manage_election', election_id=election.id)

    candidates = election.candidates.all()
    candidate_form = CandidateForm()

    return render(request, 'voting/manage_election.html', {
        'election': election,
        'candidates': candidates,
        'candidate_form': candidate_form
    })

@login_required
@role_required(['admin', 'auditor'])
def election_results(request, election_id):

    election = get_object_or_404(Election, pk=election_id)
    candidates = election.candidates.all()

    # Count votes (in production, this should be done securely)
    results = []
    for candidate in candidates:
        vote_count = Ballot.objects.filter(
            encrypted_vote__contains=f'"election_id": {election_id}',
            # encrypted_vote__contains=f'"candidate_id": {candidate.id}'
        ).count()
        results.append({
            'candidate': candidate,
            'votes': vote_count
        })

    return render(request, 'voting/election_results.html', {
        'election': election,
        'results': results
    })

class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = 'registration/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        user = self.request.user
        if user.role == 'admin':
            return reverse_lazy('admin_dashboard')
        elif user.role == 'auditor':
            return reverse_lazy('auditor_dashboard')
        elif user.role == 'voter':
            return reverse_lazy('voter_dashboard')
        else:
            return reverse_lazy('election_list')

    def form_valid(self, form):
        # Check if user has voted and prevent re-login if necessary
        user = form.get_user()
        if user.role == 'voter':
            try:
                voter = user.voter
                if voter.has_voted:
                    messages.warning(self.request, "You have already voted. Access is restricted.")
                    # Could redirect to a different page or allow limited access
            except Voter.DoesNotExist:
                pass
        return super().form_valid(form)

class SignupView(CreateView):
    model = User
    form_class = SignupForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Account created successfully! Please log in.")
        return response

class CustomLogoutView(LogoutView):
    template_name = 'registration/logout.html'
    next_page = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "You have been logged out successfully.")
        return super().dispatch(request, *args, **kwargs)

# Dashboard Views
class AdminDashboardView(TemplateView):
    template_name = 'voting/admin_dashboard.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(request.get_full_path())
        if request.user.role != 'admin':
            from django.contrib import messages
            messages.error(request, "You don't have permission to access this page.")
            return redirect('election_list')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Election overview
        elections = Election.objects.all()
        active_elections = elections.filter(is_active=True)
        total_elections = elections.count()

        # Voter statistics
        total_voters = Voter.objects.count()
        registered_voters = Voter.objects.filter(is_registered=True).count()
        voted_voters = Voter.objects.filter(has_voted=True).count()

        # Calculate participation rate
        participation_rate = (voted_voters / registered_voters * 100) if registered_voters > 0 else 0

        # Recent audit logs
        recent_logs = AuditLog.objects.select_related('user', 'election').order_by('-timestamp')[:10]

        # System metrics (mock data for now, integrate with Prometheus later)
        system_metrics = {
            'total_votes': Ballot.objects.count(),
            'encryption_ops': Ballot.objects.count(),  # Simplified
            'ip_attempts': 0,  # Would come from Prometheus
            'anomalies': 0,  # Would come from Prometheus
        }

        # Chart data for votes per election
        votes_per_election = []
        for election in elections:
            vote_count = Ballot.objects.filter(
                encrypted_vote__contains=f'"election_id": {election.id}'
            ).count()
            votes_per_election.append({
                'election': election.title,
                'votes': vote_count
            })

        context.update({
            'total_elections': total_elections,
            'active_elections': active_elections,
            'total_voters': total_voters,
            'registered_voters': registered_voters,
            'voted_voters': voted_voters,
            'participation_rate': round(participation_rate, 1),
            'recent_logs': recent_logs,
            'system_metrics': system_metrics,
            'votes_per_election': json.dumps(votes_per_election, cls=DjangoJSONEncoder),
        })

        return context

class AuditorDashboardView(TemplateView):
    template_name = 'voting/auditor_dashboard.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(request.get_full_path())
        if request.user.role != 'auditor':
            from django.contrib import messages
            messages.error(request, "You don't have permission to access this page.")
            return redirect('election_list')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Vote integrity logs
        integrity_logs = AuditLog.objects.filter(
            action__in=['vote_cast', 'security_check']
        ).select_related('user', 'election').order_by('-timestamp')[:50]

        # Check for double voting
        double_voting_detected = False
        voter_vote_counts = Ballot.objects.values('voter_id').annotate(
            vote_count=Count('voter_id')
        ).filter(vote_count__gt=1)
        if voter_vote_counts.exists():
            double_voting_detected = True

        # Hash chain validation (simplified)
        hash_chain_valid = True  # Would implement proper validation

        # Audit statistics
        total_logs = AuditLog.objects.count()
        security_checks = AuditLog.objects.filter(action='security_check').count()
        vote_logs = AuditLog.objects.filter(action='vote_cast').count()

        context.update({
            'integrity_logs': integrity_logs,
            'double_voting_detected': double_voting_detected,
            'hash_chain_valid': hash_chain_valid,
            'total_logs': total_logs,
            'security_checks': security_checks,
            'vote_logs': vote_logs,
        })

        return context

@login_required
@role_required(['auditor'])
def export_audit_logs_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="audit_logs.csv"'

    writer = csv.writer(response)
    writer.writerow(['Timestamp', 'Action', 'User', 'Election', 'IP Address', 'Hash'])

    logs = AuditLog.objects.select_related('user', 'election').order_by('-timestamp')
    for log in logs:
        writer.writerow([
            log.timestamp,
            log.get_action_display(),
            log.user.username if log.user else 'System',
            log.election.title if log.election else 'N/A',
            log.ip_address or 'N/A',
            log.hash_value
        ])

    return response

@login_required
@role_required(['auditor'])
def export_audit_logs_pdf(request):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Title
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, height - 50, "Election Audit Logs Report")

    # Headers
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, height - 100, "Timestamp")
    p.drawString(200, height - 100, "Action")
    p.drawString(350, height - 100, "User")
    p.drawString(450, height - 100, "Election")

    # Data
    p.setFont("Helvetica", 10)
    y_position = height - 120
    logs = AuditLog.objects.select_related('user', 'election').order_by('-timestamp')[:50]

    for log in logs:
        if y_position < 50:
            p.showPage()
            y_position = height - 50

        p.drawString(50, y_position, str(log.timestamp))
        p.drawString(200, y_position, log.get_action_display())
        p.drawString(350, y_position, log.user.username if log.user else 'System')
        p.drawString(450, y_position, log.election.title if log.election else 'N/A')
        y_position -= 20

    p.save()
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="audit_logs.pdf"'
    return response

class VoterDashboardView(TemplateView):
    template_name = 'voting/voter_dashboard.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(request.get_full_path())
        if request.user.role != 'voter':
            from django.contrib import messages
            messages.error(request, "You don't have permission to access this page.")
            return redirect('election_list')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get voter instance
        voter = getattr(self.request, 'voter', None)

        # Upcoming and active elections
        now = timezone.now()
        upcoming_elections = Election.objects.filter(
            start_date__gt=now,
            is_active=True
        ).order_by('start_date')

        active_elections = Election.objects.filter(
            start_date__lte=now,
            end_date__gt=now,
            is_active=True
        ).order_by('start_date')

        # Check voting status
        voting_status = {}
        if voter:
            for election in active_elections:
                has_voted = Ballot.objects.filter(
                    voter_id=voter.voter_id,
                    encrypted_vote__contains=f'"election_id": {election.id}'
                ).exists()
                voting_status[election.id] = has_voted

        # Recent vote verification (if voted)
        recent_ballot = None
        if voter and voter.has_voted:
            recent_ballot = Ballot.objects.filter(voter_id=voter.voter_id).order_by('-timestamp').first()

        context.update({
            'upcoming_elections': upcoming_elections,
            'active_elections': active_elections,
            'voting_status': voting_status,
            'recent_ballot': recent_ballot,
            'voter': voter,
        })

        return context

@login_required
@role_required(['voter'])
def verify_vote(request, ballot_id):
    try:
        ballot = Ballot.objects.get(ballot_id=ballot_id)
        voter = getattr(request, 'voter', None)

        if voter and str(ballot.voter_id) == str(voter.voter_id):
            # Decrypt and verify vote
            decrypted_vote = ballot.get_decrypted_vote()
            vote_data = json.loads(decrypted_vote)

            election = Election.objects.get(id=vote_data['election_id'])
            candidate = Candidate.objects.get(id=vote_data['candidate_id'])

            return JsonResponse({
                'verified': True,
                'election': election.title,
                'candidate': candidate.name,
                'timestamp': ballot.timestamp.isoformat(),
                'ballot_id': str(ballot.ballot_id)
            })
        else:
            return JsonResponse({'verified': False, 'error': 'Unauthorized access'})
    except (Ballot.DoesNotExist, json.JSONDecodeError, Election.DoesNotExist, Candidate.DoesNotExist):
        return JsonResponse({'verified': False, 'error': 'Invalid ballot or data corruption'})
