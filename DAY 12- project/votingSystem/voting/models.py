import uuid
from django.db import models
from django.contrib.auth.models import User
from cryptography.fernet import Fernet
import os

# Generate a key for encryption (in production, store this securely)
ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY', Fernet.generate_key())
cipher = Fernet(ENCRYPTION_KEY)

class Voter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    voter_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    is_registered = models.BooleanField(default=False)
    registration_date = models.DateTimeField(auto_now_add=True)

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
