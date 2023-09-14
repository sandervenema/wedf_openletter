from django.shortcuts import get_object_or_404, render, redirect
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from django.template import loader
from django.utils import translation
from django.utils.translation import gettext as _

import hashlib
import time
import logging
from smtplib import SMTPException
import requests_cache
import markdown
from bs4 import BeautifulSoup

from .models import Petition, Signature, Suggestion
from .forms import PetitionForm, SuggestionForm


# get logging instance and set formatter
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s')


# Fetch latest Markdown source of open letter from Github
# Cache this so we don't hit the server on every request.
def fetch_latest_letter(url, lang='en'):
    with requests_cache.CachedSession(backend='sqlite', expire_after=settings.LETTER_GH_EXPIRES_AFTER) as session:
        if lang == 'en':
            resp = session.get(settings.LETTER_GH_URL)
        else:
            resp = session.get(settings.LETTER_GH_URL.replace('.md', '_' + lang + '.md'))
        if resp.status_code != 200:
            md_src = "# Could not retrieve letter\n\nPlease go [here]({}) to see it.".format(
                settings.LETTER_GH_URL_PRETTY)
        else:
            md_src = resp.text
    letter_text = markdown.markdown(md_src, output_format='html')
    soup = BeautifulSoup(letter_text, 'html.parser')

    # If we don't have h3s, just skip the next bit:
    if not soup.find('h3'):
        return str(soup)

    # Wrap everthing from the first <h3> until the end of the document in a div.
    accordion_div = soup.new_tag('div', attrs={'id': 'accordion'})
    prev_sibling = soup.find('h3').previous_sibling
    next_siblings = list(prev_sibling.next_siblings)
    for sibling in next_siblings:
        accordion_div.append(sibling)
    prev_sibling.insert_after(accordion_div)

    # Wrap everything after <h3> in a div until the next <h3>.
    h3s = soup.find_all('h3')
    for h3 in h3s:
        panel_div = soup.new_tag('div')
        for sibling in list(h3.next_siblings):
            if sibling.name == 'h3':
                break
            panel_div.append(sibling)
        h3.insert_after(panel_div)

    return str(soup)


def index(request):
    # set language explicitly if we specify a language in URL
    available_languages = [code for (code, trans) in settings.LANGUAGES]
    if request.LANGUAGE_CODE is not None and request.LANGUAGE_CODE in available_languages:
        translation.activate(request.LANGUAGE_CODE)
        request.LANGUAGE_CODE = translation.get_language()

    petition = get_object_or_404(Petition, pk=1)
    initial_signatures = petition.signature_set.filter(active=True,
            initial=True).order_by('order', 'name')
    active_signatures = petition.signature_set.filter(active=True,
            initial=False).order_by('-timestamp')
    form = PetitionForm()
    suggestion_form = SuggestionForm()
    letter_text = fetch_latest_letter(url=settings.LETTER_GH_URL, language=request.LANGUAGE_CODE)

    return render(request, 'petitions/index.html', {
        'letter_text': letter_text,
        'petition': petition, 
        'signatures': active_signatures,
        'initial_signatures': initial_signatures,
        'form': form,
        'suggestion_form': suggestion_form}) 


def sign(request):
    petition = get_object_or_404(Petition, pk=1)

    if request.method == 'POST':
        form = PetitionForm(request.POST)

        if form.is_valid():
            # Get values from form
            email = form.cleaned_data['email']
            name = form.cleaned_data['name']
            affil = form.cleaned_data['affiliation']
            job_title = form.cleaned_data['job_title']
            timestamp = time.time()
            hash_val = hashlib.sha256(' '.join([email, name, 
                affil, str(timestamp)]).encode('utf-8')).hexdigest()

            # Add values to db
            s = Signature(email=hashlib.sha256(email.encode()).hexdigest(),
                    name=name, job_title=job_title, affiliation=affil, petition=petition, link=hash_val)
            s.save()

            # Generate confirmation url
            link = request.build_absolute_uri(reverse('confirm', 
                urlconf=None, args=[hash_val]))

            # Make a confirmation message
            subject = _('WEDF: Confirm your signature')
            to_addr = [email]
            from_addr = 'no-reply@worldethicaldata.org'
            message_templ = loader.get_template('petitions/confirmation_mail.txt')
            message = message_templ.render({'link': link, 'name': name})

            # Send confirmation e-mail to sender
            try:
                send_mail(subject, message, from_addr, to_addr)
            except SMTPException:
                # mail NOT delivered! log details
                logger.exception("Mail not sent! "
                             "(input params: subject={}, from_addr={}, to_addr={}, message={}"
                             .format(subject, from_addr, to_addr, message))
                # render the thank you page, but with a confirm link to confirm
                # manually.
                return render(request, 'petitions/thankyou.html', {'confirmlink': link})

            # Display thank you message
            return render(request, 'petitions/thankyou.html')
        else:
            initial_signatures = petition.signature_set.filter(active=True,
                    initial=True).order_by('name')
            active_signatures = petition.signature_set.filter(active=True,
                    initial=False).order_by('-timestamp')
            suggestion_form = SuggestionForm()
            letter_text = fetch_latest_letter(settings.LETTER_GH_URL)

            return render(request, 'petitions/index.html', {
                'letter_text': letter_text,
                'petition': petition, 
                'signatures': active_signatures,
                'initial_signatures': initial_signatures,
                'form': form,
                'suggestion_form': suggestion_form}) 
    else:
        # redirect to index
        return redirect('index')


# Confirmation
def confirm(request, link):
    # Bug in uwsgi: always read request data even if you don't need it, otherwise things get clobbered:
    _data = request.POST

    # Set db sig to active
    s = get_object_or_404(Signature, link=link)
    s.active = True
    s.save()

    # Display thank you message + confirm message
    return render(request, 'petitions/confirmed.html')


# Make a suggestion
def suggest(request):
    petition = get_object_or_404(Petition, pk=1)

    if request.method == 'POST':
        form = SuggestionForm(request.POST)

        if form.is_valid():
            # Get values from form
            suggestion = form.cleaned_data['suggestion']
            name = form.cleaned_data['name']
            affil = form.cleaned_data['affiliation']
            job_title = form.cleaned_data['job_title']
            email = form.cleaned_data['email']

            # Add values to db
            s = Suggestion(suggestion=suggestion,
                    name=name, job_title=job_title, affiliation=affil, email=email, petition=petition)
            s.save()

            # Display thank you message
            return render(request, 'petitions/thankyou-suggestion.html')
        else:
            initial_signatures = petition.signature_set.filter(active=True,
                    initial=True).order_by('name')
            active_signatures = petition.signature_set.filter(active=True,
                    initial=False).order_by('-timestamp')
            petition_form = PetitionForm()
            letter_text = fetch_latest_letter(settings.LETTER_GH_URL)

            return render(request, 'petitions/index.html', {
                'letter_text': letter_text,
                'petition': petition, 
                'signatures': active_signatures,
                'initial_signatures': initial_signatures,
                'form': petition_form,
                'suggestion_form': form}) 
    else:
        # redirect to index
        return redirect('index')