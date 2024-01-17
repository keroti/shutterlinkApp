from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse
from .models import Services, PhotographerProfile


# Create your views here.
def index(request):
    return render(request, 'index.html')


def profileMain(request):
    services = Services.objects.all()
    return render(request, 'profileMain.html', {'services': services})

def create_profile(request):
    if request.method == 'POST':
        return redirect('/profile')  # Redirect to the profile page
    else:
        return render(request, 'profile1.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if username and email and password and password2:
            if len(password) < 8 or len(password) > 20:
                messages.error(request, 'Password must be between 8 and 20 characters long')
                return redirect('register')

            if password == password2:
                if User.objects.filter(username=username).exists():
                    messages.error(request, 'Username Already Taken')
                    return redirect('register')
                elif User.objects.filter(email=email).exists():
                    messages.error(request, 'Email Already Taken')
                    return redirect('register')
                else:
                    user = User.objects.create_user(username=username, email=email, password=password)
                    user.save()
                    return redirect('login')
            else:
                messages.error(request, 'Passwords do not match')
                return redirect('register')
        else:
            messages.error(request, 'Please fill in all the required fields')
            return redirect('register')
    else:
        return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('/profile')
            else:
                messages.error(request, 'Invalid Credentials')
                return redirect('login')
        else:
            messages.error(request, 'Please fill in all the required fields')
            return redirect('login')
    else:
        return render(request, 'login.html')


def logout_view(request):
    auth.logout(request)
    return redirect('login')


class CreateOrUpdatePhotographerProfileView(LoginRequiredMixin, UpdateView):
    model = PhotographerProfile
    template_name = 'profile1.html'
    fields = ['profile_pic', 'name', 'bio', 'birth_date', 'contact_information', 'email', 'twitter', 'facebook', 'instagram', 'linkedin', 'occupation', 'website', 'city', 'country', 'service_name', 'service_details']

    def get_object(self, queryset=None):
        # Get the existing profile for the current user or create a new one
        profile, created = PhotographerProfile.objects.get_or_create(user=self.request.user)
        return profile
    
    def form_valid(self, form):
        # Save the form data to the database
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        # Return the URL to redirect to after a successful form submission
        return reverse('edit_profile')

@login_required
def profileMain(request):
    # Filter PhotographerProfile objects for the currently authenticated user
    update_profiles = PhotographerProfile.objects.filter(user=request.user)
    return render(request, 'profileMain.html', {'update_profiles': update_profiles})


def search(request):
    # Get the search query from the request's GET parameters
    query = request.GET.get('q')

    # Initialize an empty list to store search results
    search_results = []

    if query:
        # Perform a case-insensitive search for profiles based on the name field
        search_results = PhotographerProfile.objects.filter(name__icontains=query)

    # Render the 'search.html' template with the query and search results
    return render(request, 'search.html', {'query': query, 'search_results': search_results})


def profile_detail(request, name):
    # Retrieve the profile based on the name
    profile = get_object_or_404(PhotographerProfile, name=name)

    return render(request, 'profile_detail.html', {'profile': profile})
