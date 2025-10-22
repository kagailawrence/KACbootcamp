from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .models import Voter, Ballot, Election, Candidate, User, EligibleVoter

class VoterRegistrationForm(forms.ModelForm):
    class Meta:
        model = Voter
        fields = ['user']
        widgets = {
            'user': forms.HiddenInput(),
        }

class VoteForm(forms.Form):
    candidate = forms.ModelChoiceField(
        queryset=Candidate.objects.none(),
        widget=forms.RadioSelect,
        empty_label=None
    )

    def __init__(self, election, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['candidate'].queryset = Candidate.objects.filter(election=election)

class ElectionForm(forms.ModelForm):
    class Meta:
        model = Election
        fields = ['title', 'description', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=254,
        widget=forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'})
    )

class SignupForm(UserCreationForm):
    national_id = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'})
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'national_id', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'first_name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'}),
        }

    def clean_national_id(self):
        national_id = self.cleaned_data.get('national_id')
        email = self.cleaned_data.get('email')

        # Check if eligible voter exists
        try:
            eligible_voter = EligibleVoter.objects.get(
                national_id=national_id,
                email=email,
                is_active=True
            )
        except EligibleVoter.DoesNotExist:
            raise ValidationError("You are not eligible to register. Please contact election officials.")

        # Check if user already exists
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists.")

        return national_id

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'voter'  # Default role for new signups
        if commit:
            user.save()
        return user
