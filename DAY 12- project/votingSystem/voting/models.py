import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from cryptography.fernet import Fernet
import os

# Generate a key for encryption (in production, store this securely)
ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY', Fernet.generate_key())
cipher = Fernet(ENCRYPTION_KEY)

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('auditor', 'Auditor'),
        ('voter', 'Voter'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='voter')

    class Meta:
        db_table = 'auth_user'

class EligibleVoter(models.Model):
    national_id = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} ({self.national_id})"

    class Meta:
        verbose_name = "Eligible Voter"
        verbose_name_plural = "Eligible Voters"
        indexes = [
            models.Index(fields=['national_id']),
            models.Index(fields=['email']),
        ]

class Voter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    voter_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    is_registered = models.BooleanField(default=False)
    registration_date = models.DateTimeField(auto_now_add=True)
    has_voted = models.BooleanField(default=False)  # Track if voter has voted

    def __str__(self):
        return f"Voter: {self.user.username}"

    class Meta:
        verbose_name = "Voter"
        verbose_name_plural = "Voters"

class Ballot(models.Model):
    ballot_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    voter_id = models.UUIDField()  # Anonymous reference to voter
    encrypted_vote = models.TextField()  # Encrypted vote data
    timestamp = models.DateTimeField(auto_now_add=True)
    is_counted = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Encrypt the vote before saving
        if not self.pk:  # Only encrypt on creation
            self.encrypted_vote = cipher.encrypt(self.encrypted_vote.encode()).decode()
        super().save(*args, **kwargs)

    def get_decrypted_vote(self):
        return cipher.decrypt(self.encrypted_vote.encode()).decode()

    def __str__(self):
        return f"Ballot: {self.ballot_id}"

    class Meta:
        verbose_name = "Ballot"
        verbose_name_plural = "Ballots"
        indexes = [
            models.Index(fields=['voter_id']),
            models.Index(fields=['timestamp']),
        ]

class Election(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Election"
        verbose_name_plural = "Elections"

class Candidate(models.Model):
    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name='candidates')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} - {self.election.title}"

    class Meta:
        verbose_name = "Candidate"
        verbose_name_plural = "Candidates"
        unique_together = ('election', 'name')

class AuditLog(models.Model):
    ACTION_CHOICES = [
        ('vote_cast', 'Vote Cast'),
        ('election_created', 'Election Created'),
        ('election_started', 'Election Started'),
        ('election_ended', 'Election Ended'),
        ('candidate_added', 'Candidate Added'),
        ('security_check', 'Security Check'),
    ]

    timestamp = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    election = models.ForeignKey(Election, on_delete=models.SET_NULL, null=True, blank=True)
    details = models.JSONField()  # Store additional metadata
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    hash_value = models.CharField(max_length=128, blank=True)  # For integrity verification

    def save(self, *args, **kwargs):
        if not self.hash_value:
            import hashlib
            hash_data = f"{self.timestamp}{self.action}{self.user_id or ''}{self.election_id or ''}{self.details}"
            self.hash_value = hashlib.sha256(hash_data.encode()).hexdigest()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.action} - {self.timestamp}"

    class Meta:
        verbose_name = "Audit Log"
        verbose_name_plural = "Audit Logs"
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['timestamp']),
            models.Index(fields=['action']),
            models.Index(fields=['election']),
        ]

class SystemMetrics(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    metric_name = models.CharField(max_length=100)
    value = models.FloatField()
    labels = models.JSONField(blank=True, null=True)  # Additional metadata

    def __str__(self):
        return f"{self.metric_name}: {self.value} at {self.timestamp}"

    class Meta:
        verbose_name = "System Metric"
        verbose_name_plural = "System Metrics"
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['timestamp']),
            models.Index(fields=['metric_name']),
        ]
