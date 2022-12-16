from django.shortcuts import render
from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.shortcuts import get_object_or_404
from .models import Bunk, User

class UserListView(generic.ListView):
    template_name = 'jitter/user_list.html'
    context_object_name = 'user_list'

    def get_queryset(self):
        """Return the list of users"""
        return User.objects.all()

class BunkView(generic.ListView):
    template_name = 'jitter/bunks.html'
    context_object_name = 'bunk_list'

    def get_queryset(self):
        return Bunk.objects.all()

class UserBunkView(generic.TemplateView):
    template_name = "jitter/user.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, pk=kwargs["user_id"])
        context["user"] = user
        context["bunk_list"] = user.to_set.all()
        context["users"] = User.objects.all()
        return context

def add_bunk(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    from_user = get_object_or_404(User, pk=request.POST['from_user'])
    bunk= Bunk(from_user=from_user, to_user=user, time=timezone.now())
    bunk.save()
    return HttpResponseRedirect(reverse('jitter:user', args=(user.id,)))


