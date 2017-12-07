from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import auth
from django.utils import html
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.forms import ModelForm
from django.conf import settings
from .models import Subscription, Profile, Pokemon
from .forms import AccountForm, AccountEditForm,ProfileEditForm


# Create your views here.
def index(request):
    result = Profile.objects.filter(user=request.user)
    context = {'nbar': 'home',
                'heading': 'PokeDex Online',
                'mission': 'Your #1 Source For Pokemon Information',
                'pokemons': result[0].favorites.all,
            }
    return render(request, 'pokemon/index.html', context)

def book_list(request):

    context = {
        'nbar': 'pokedex',
        'pageTitle': 'Pokemon',
        'pokemons': Pokemon.objects.all(),
    }
    return render(request, 'pokemon/list.html', context)

@login_required
def add_to_cart(request,book_id):
    return HttpResponseRedirect('index')


def subscribe(request):
    errors = []
    context = {}
    if 'email' in request.GET:
        email_id = request.GET.get('email', '')
        if not email_id:
            errors.append('Please enter a valid email address.')
        else:
            subs = Subscription.objects.create(email=email_id)
            context['pageTitle']= 'Thank you!'
            context['panelTitle'] = 'Thank you!'
            context['panelBody'] = 'Thank you for subscribing to our mailing list.'
            return render(request, 'pokemon/static.html', context)
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def contact(request):
    context = {
        'nbar': 'contact',
        'pageTitle': 'Contact',
        'panelTitle': 'Contact',
        'panelBody': """
            <!-- List group -->
            <ul class="list-group">
            <li class="list-group-item"><strong>Professor Oak: </strong><br />
                <address>123 Oak Drive<br>
                        Pallet Town, Kanto <br>
                        &phone;: (123)-456-7890<br>
                        <span class="glyphicon glyphicon-envelope"></span>: oak@professor.com<br>
                </address>
            
        """,
    }
    return render(request, 'pokemon/static.html', context)

def login(request):
    # print('site = ', request.get_host())
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        valid = False
        error_message = []
        if not username or not password:
            error_message = ['You must fill in all of the fields.']
        else:
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    # correct password, and the user is marked active
                    auth.login(request, user)
                    request.session['user_id'] = user.id
                    valid = True
                else:
                    error_message = ["User accocount has not been activated."]

            else:
                error_message = ["Invalid username or password."]

        if valid:
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request,
                          'pokemon/login.html',
                          {
                           'errorMessage': ' '.join(error_message),
                           'username': username,
                           'password': password,
                           })

    else:
        # No context variables to pass to the template system, hence blank
        # dictionary object...
        return render(request,
                      'pokemon/login.html',
                      {
                          'pageTitle': 'Login',
                      })

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))

def addboitolist(request):
    return HttpResponseRedirect('index')

def signup(request):
    valid = False
    error_message = []
    message_type = 'info'
    # path = request.get_full_path()
    # print('path = ', path)
    if request.user.is_authenticated():
        # user already has an account and is authenticated; don't let them register again
        error_message = [u'''You are logged in as {username}. If you'd like to register another account,
                         <a href="{url}">Logout</a> first.
                         '''.format(username=html.escape(request.user.username), url=settings.LOGOUT_URL)]
        valid = False
    # If it's a HTTP POST, we're interested in processing form data.
    elif request.method == 'POST':
        accForm = AccountForm(data=request.POST)
        if accForm.is_valid():
            # check for duplicate username
            user = auth.models.User.objects.filter(username=accForm.cleaned_data['username'])
            if user:
                url = '/recover/' # not implemented
                error_message = [u'''Account with email {username} already exists. <a href="{url}">
                                 Forgot your password? </a>
                                 '''.format(username=html.escape(accForm.cleaned_data['username']), url=url)]
                valid = False
            else:
                try:
                    validate_password(accForm.cleaned_data['password'])
                    valid = True
                except ValidationError as ex:
                    valid = False
                    for e in ex: #ex is list of error messages
                        error_message.append(e)
        else:
            valid = False
            for k in accForm.errors:
                error_message.append('<br>'.join(accForm.errors[k]))

        if valid:
            # Save the user's form data to the built-in user table.
            user = accForm.save(commit=False)
            user.set_password(accForm.cleaned_data['password']) # set the password using default hashing
            user.is_active = True #set it to False if verifcation is required
            user.is_superuser = False
            user.is_staff = False
            user.save()
            # save user to profile table as well
            profile = Profile(user=user)
            profile.save()
            # generate_activation_key_and_send_email(site_url, user)
            # send_mail(subject, message, from_email, to_list, html_message=html_message, fail_silently=True)
            # Update our variable to tell the template registration was successful.
            error_message = [u'''The account is created. Follow the link to login...<a
                                     href="{url}">Login</a>.
                                     '''.format(url=reverse('login'))]
            return render(request,
                        'pokemon/message.html',
                        {
                            'pageTitle': 'Feedback',
                            'messageType': 'success',
                            'message': ' '.join(error_message),
                        })

        else:
            return render(request,
                        'pokemon/signup.html',
                        {
                            'pageTitle': 'Account Registration',
                            'panelTitle': 'Account Registration',
                            'accountForm': accForm,
                            'errorMessage': '<br>'.join(error_message),
                        })

        
    else:
        accForm = AccountForm()
        return render(request,
                      'pokemon/signup.html',
                      {
                          'pageTitle': 'Account Registration',
                          'panelTitle': 'Account Registration',
                          'accountForm': accForm,
                      })


def search(request):
    context = {}
    if 'search' in request.GET:
        q = request.GET.get('search', '')
        if q:
            pokemon = Pokemon.objects.filter(name__icontains=q)
            context['pageTitle']= 'Search results'
            context['panelTitle'] = '%d matching results'%len(pokemon)
            context['pokemons'] = pokemon
            return render(request, 'pokemon/search_results.html', context)
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))