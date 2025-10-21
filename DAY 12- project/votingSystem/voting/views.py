import json
import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import Voter, Ballot, Election, Candidate
from .forms import VoterRegistrationForm, VoteForm, ElectionForm, CandidateForm

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

            messages.success(request, "Your vote has been recorded anonymously.")
            return redirect('election_list')
    else:
        form = VoteForm(election)

    return render(request, 'voting/vote.html', {'form': form, 'election': election})

# Admin views
@login_required
def create_election(request):
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to create elections.")
        return redirect('election_list')

    if request.method == 'POST':
        form = ElectionForm(request.POST)
        if form.is_valid():
            election = form.save()
            messages.success(request, f"Election '{election.title}' created successfully.")
            return redirect('manage_election', election_id=election.id)
    else:
        form = ElectionForm()

    return render(request, 'voting/create_election.html', {'form': form})

@login_required
def manage_election(request, election_id):
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to manage elections.")
        return redirect('election_list')

    election = get_object_or_404(Election, pk=election_id)

    if request.method == 'POST':
        if 'activate' in request.POST:
            election.is_active = True
            election.save()
            messages.success(request, "Election activated.")
        elif 'deactivate' in request.POST:
            election.is_active = False
            election.save()
            messages.success(request, "Election deactivated.")
        elif 'add_candidate' in request.POST:
            candidate_form = CandidateForm(request.POST)
            if candidate_form.is_valid():
                candidate = candidate_form.save(commit=False)
                candidate.election = election
                candidate.save()
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
def election_results(request, election_id):
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to view results.")
        return redirect('election_list')

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
