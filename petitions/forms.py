import hashlib

from django import forms
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


from .models import Signature, Suggestion


def validate_duplicate_email(email):
    # Get all hashes from the database and check whether there is a match.
    hashes = [e[0] for e in Signature.objects.values_list('email').all()]
    email_hash = hashlib.sha256(email.encode()).hexdigest()
    if email_hash in hashes:
        raise ValidationError(_("You can only submit the petition once!"))


class PetitionForm(forms.Form):
    name = forms.CharField(label='', 
                           widget=forms.TextInput(attrs={'placeholder': _('Your name *')}), 
                           max_length=200)
    job_title = forms.CharField(label='',
                           widget=forms.TextInput(attrs={'placeholder': _('Your title')}), 
                           max_length=200, required=False)
    affiliation = forms.CharField(label='',
                           widget=forms.TextInput(attrs={'placeholder': _('Your affiliation')}), 
                           max_length=200, required=False)
    email = forms.EmailField(label='', 
                           widget=forms.TextInput(attrs={'placeholder': _('Your e-mail address *')}),
                           validators=[validate_duplicate_email])


class SuggestionForm(forms.Form):
    suggestion = forms.CharField(label='', 
                           widget=forms.Textarea(attrs={'placeholder': _('Please type your suggestion here.')}),
                           max_length=10000)
    name = forms.CharField(label='', 
                           widget=forms.TextInput(attrs={'placeholder': _('Your name *')}), 
                           max_length=200)
    job_title = forms.CharField(label='',
                           widget=forms.TextInput(attrs={'placeholder': _('Your title')}), 
                           max_length=200, required=False)
    affiliation = forms.CharField(label='',
                           widget=forms.TextInput(attrs={'placeholder': _('Your affiliation')}), 
                           max_length=200, required=False)
    email = forms.EmailField(label='', 
                           widget=forms.TextInput(attrs={'placeholder': _('Your e-mail address')}),
                           required=False,
                           validators=[EmailValidator])
