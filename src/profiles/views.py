from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView, View

from restaurants.models import RestaurantLocation
from menus.models import Item
from .models import Profile

User = get_user_model()


class ProfileDetailView(DetailView):
    template_name = 'profiles/user.html'

    def get_object(self, **kwargs):
        username = self.kwargs.get("username")
        if username is None:
            raise Http404
        return get_object_or_404(User, username__iexact=username, is_active=True)

    def get_context_data(self, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(**kwargs)
        user = context['user']
        query = self.request.GET.get("q")
        is_following = False

        if user.profile in self.request.user.is_following.all():
            is_following = True

        context['is_following'] = is_following

        items_exist = Item.objects.filter(user=user).exists()
        qs = RestaurantLocation.objects.filter(owner=user).search(query)

        if items_exist and qs.exists():
            context['locations'] = qs

        return context


class ProfileFollowToggle(LoginRequiredMixin, View):
    def post(self, request, **kwargs):
        user_to_toggle = request.POST.get("username")
        profile_, is_following = Profile.objects.toggle_follow(request.user, user_to_toggle)

        return redirect(f"/profiles/{profile_.user.username}/")
