from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login
from django.views.generic import View, TemplateView
from .forms import UserForm
from django.views import generic
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.contrib import messages
import random


def index(request):
    return render(request, 'index.html')


class Profile(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super(Profile, self).get_context_data(**kwargs)
        context['team'] = Team.objects.filter(user=self.request.user)
        return context


class Settings(LoginRequiredMixin, TemplateView):
    template_name = 'settings.html'

    def get_context_data(self, **kwargs):
        context = super(Settings, self).get_context_data(**kwargs)
        context['select_list'] = UserSelect.objects.filter(user=self.request.user)
        context['team'] = Team.objects.filter(user=self.request.user)
        return context


class BowlerListView(LoginRequiredMixin, generic.ListView):
    model = Bowler
    context_object_name = 'bowler_list'  # your own name for the list as a template variable
    template_name = 'bowlers.html'

    def get_context_data(self, **kwargs):
        context = super(BowlerListView, self).get_context_data(**kwargs)
        context['select_list'] = UserSelect.objects.filter(user=self.request.user)
        context['team'] = Team.objects.filter(user=self.request.user)
        return context

    def get_queryset(self):
        return Bowler.objects.all()


class BatsmanListView(LoginRequiredMixin, generic.ListView):
    model = Batsman
    context_object_name = 'batsman_list'  # your own name for the list as a template variable
    template_name = 'batsmen.html'

    def get_context_data(self, **kwargs):
        context = super(BatsmanListView, self).get_context_data(**kwargs)
        context['select_list'] = UserSelect.objects.filter(user=self.request.user)
        context['team'] = Team.objects.filter(user=self.request.user)
        return context

    def get_queryset(self):
        return Batsman.objects.all()


def detail(request, pk):
    if not request.user.is_authenticated():
        return render(request, 'registration/login.html')
    else:
        bowler = get_object_or_404(Bowlers, pk=pk)
        select_list = UserSelect.objects.filter(user=request.user, bowler=pk)
        all_select = UserSelect.objects.filter(user=request.user).count()
        team = Team.objects.filter(user=request.user)
        context = {
            'bowler': bowler,
            'select_list': select_list,
            'all_select': all_select,
            'team': team,
        }
        return render(request, 'bowler_detail.html', context)


class BowlerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Bowler
    template_name = 'bowler_detail.html'

    def get_context_data(self, **kwargs):
        context = super(BowlerDetailView, self).get_context_data(**kwargs)
        context['select_list'] = UserSelect.objects.filter(user=self.request.user, bowler=self.kwargs.get('pk'))
        context['all_select'] = UserSelect.objects.filter(user=self.request.user).count()
        context['team'] = Team.objects.filter(user=self.request.user)
        return context


class BatsmanDetailView(LoginRequiredMixin, generic.DetailView):
    model = Batsman
    template_name = 'batsman_detail.html'

    def get_context_data(self, **kwargs):
        context = super(BatsmanDetailView, self).get_context_data(**kwargs)
        context['select_list'] = UserSelect.objects.filter(user=self.request.user, batsman=self.kwargs.get('pk'))
        context['all_select'] = UserSelect.objects.filter(user=self.request.user).count()
        context['team'] = Team.objects.filter(user=self.request.user)
        return context


def select_bowler(request, pk):
        bowler = get_object_or_404(Bowlers, pk=pk)
        team2 = Team.objects.get(user=request.user)
        if UserSelect.objects.filter(user=request.user, bowler=bowler,).exists():
            messages.error(request, 'Already selected')
            return redirect(reverse('bowler-detail', args=(pk,)))
        else:
            UserSelect.objects.create(user=request.user, bowler=bowler, team=team2.arr[team2.counter])
            if team2.counter == team2.total-1:
                team2.counter = 0
                team2.save()
            else:
                team2.counter = team2.counter+1
                team2.save()
            return redirect(reverse('bowler-detail', args=(pk,)))


def select_batsman(request, pk):
    bowler = get_object_or_404(Batsman, pk=pk)
    team2 = Team.objects.get(user=request.user)
    if UserSelect.objects.filter(user=request.user, batsman=bowler, ).exists():
        messages.error(request, 'Already selected')
        return redirect(reverse('batsman-detail', args=(pk,)))
    else:
        UserSelect.objects.create(user=request.user, batsman=bowler, team=team2.arr[team2.counter])
        if team2.counter == team2.total - 1:
            team2.counter = 0
            team2.save()
        else:
            team2.counter = team2.counter + 1
            team2.save()
        return redirect(reverse('batsman-detail', args=(pk,)))


def select_team(request):
    if request.method == 'POST':
        total = request.POST.get('team_number')
        a = int(total)+1
        arr = random.sample(range(1, a), int(total))
        team = Team.objects.create(user=request.user, total=total, arr=arr)
        team.save()
        return redirect(reverse('profile', args=()))
    return render(request, 'profile.html')


def reset_all(request):  # reset player and teams
    Team.objects.filter(user=request.user).delete()
    UserSelect.objects.filter(user=request.user).delete()
    return redirect(reverse('settings', args=()))


def reset_pl(request):  # resets only all players
    Team.objects.filter(user=request.user).update(counter=0)
    UserSelect.objects.filter(user=request.user).delete()
    return redirect(reverse('settings', args=()))


class UserFormView(View):
    form_class = UserForm
    template_name = 'registration_form.html'

# display blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

# process
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)

            if user is not None:

                if user.is_active:
                    login(request, user)
                    return redirect('home')

        return render(request, self.template_name, {'form': form})


class SelectedByUserListView(LoginRequiredMixin, generic.ListView):
    model = UserSelect
    template_name = 'teams.html'
    context_object_name = 'select_list'

    def get_queryset(self):
        return UserSelect.objects.filter(user=self.request.user)
