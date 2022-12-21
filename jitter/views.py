from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ImageField
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import reverse_lazy
from django.utils import timezone
from django.views import generic

from .models import Bunk, JitterbunkUser


class UserListView(generic.ListView):
    template_name = 'jitter/user_list.html'
    context_object_name = 'user_list'

    def get_queryset(self):
        """Return the list of users"""
        return JitterbunkUser.objects.all()

class BunkView(generic.ListView):
    template_name = 'jitter/all_bunks.html'
    context_object_name = 'bunk_list'

    def get_queryset(self):
        return Bunk.objects.all().order_by('-time')

class UserBunkView(generic.TemplateView):
    template_name = "jitter/user_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(JitterbunkUser, pk=kwargs["user_id"])
        context["user"] = user
        context["bunks_recieved"] = user.bunks_recieved.all().order_by('-time')
        context["bunks_given"] = user.bunks_sent.all().order_by('-time')
        context["users"] = JitterbunkUser.objects.all()
        return context

def add_bunk(request, user_id):
    user = get_object_or_404(JitterbunkUser, pk=user_id)
    from_user = get_object_or_404(JitterbunkUser, pk=request.user.id)
    bunk = Bunk(from_user=from_user, to_user=user, time=timezone.now())
    bunk.save()
    print("Bunking", user_id, request.user.id)
    return HttpResponseRedirect(reverse('jitter:user_page', args=(user.id,)))

class SignUpView(generic.CreateView):
    model = User
    form_class = UserCreationForm
    success_url = reverse_lazy("jitter:login")
    template_name = "registration/signup.html"

class JitterbunkUserForm(forms.Form):
    photo = forms.ImageField()

def update_profile(request):
    if request.method == 'POST':
        jitterbunk_user_form = JitterbunkUserForm(request.POST, request.FILES)
        if jitterbunk_user_form.is_valid():
            print(jitterbunk_user_form.cleaned_data.get('photo'))
            request.user.jitterbunkuser.photo = jitterbunk_user_form.cleaned_data.get('photo')
            request.user.save()
            return HttpResponseRedirect(reverse('jitter:user_page', args=(request.user.id, )))
    else:
        jitterbunk_user_form = JitterbunkUserForm()
    return render(request, 'registration/profile.html', {
        'jitterbunk_user_form': jitterbunk_user_form
    })
