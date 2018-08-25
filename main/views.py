from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import View, TemplateView
from .forms import UserForm
from django.views import generic
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.contrib import messages
import random
from .fusioncharts import FusionCharts
from django.core.mail import send_mail
from django.conf import settings


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


def bowler_detail(request, pk):
    if not request.user.is_authenticated():
        return render(request, 'registration/login.html')
    else:
        bowler = Bowlers.objects.get(pk=pk)
        select_list = UserSelect.objects.filter(user=request.user, bowler=pk)
        all_select = UserSelect.objects.filter(user=request.user).count()
        team = Team.objects.filter(user=request.user)
        dataSource = {}
        dataSource['chart'] = {
            "caption": "last year",
            "subCaption": "Harry's SuperMart",
            "xAxisName": "Month",
            "yAxisName": "Revenues (In USD)",
            "numberPrefix": "$",
            "theme": "zune",
            "type": "doughnut2d"
        }
        dataSource['data'] = []
        # Iterate through the data in `Revenue` model and insert in to the `dataSource['data']` list.
        data = {}
        data['label'] = bowler.name
        data['value'] = bowler.ave
        dataSource['data'].append(data)
        column2D = FusionCharts("doughnut2d", "ex1", "600", "350", "chart-1", "json", dataSource)
        context = {
            'bowler': bowler,
            'select_list': select_list,
            'all_select': all_select,
            'team': team,
            'output': column2D.render()
        }
        return render(request, 'bowler_detail.html', context)


def batsman_detail(request, pk):
    if not request.user.is_authenticated():
        return render(request, 'registration/login.html')
    else:
        batsman = Batsmen.objects.get(pk=pk)
        select_list = UserSelect.objects.filter(user=request.user, batsman=pk)
        all_select = UserSelect.objects.filter(user=request.user).count()
        team = Team.objects.filter(user=request.user)
        context = {
            'batsman': batsman,
            'select_list': select_list,
            'all_select': all_select,
            'team': team,
        }
        return render(request, 'batsman_detail.html', context)


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
    batsman = get_object_or_404(Batsmen, pk=pk)
    team2 = Team.objects.get(user=request.user)
    if UserSelect.objects.filter(user=request.user, batsman=batsman, ).exists():
        messages.error(request, 'Already selected')
        return redirect(reverse('batsman-detail', args=(pk,)))
    else:
        UserSelect.objects.create(user=request.user, batsman=batsman, team=team2.arr[team2.counter])
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
                    return redirect('profile')

        return render(request, self.template_name, {'form': form})


class SelectedByUserListView(LoginRequiredMixin, generic.ListView):
    model = UserSelect
    template_name = 'teams.html'
    context_object_name = 'select_list'

    def get_queryset(self):
        return UserSelect.objects.filter(user=self.request.user)


def email_username(request):
    user = User.objects.get(email=request.POST['email'])
    subject = 'Forgot your username'
    message = 'Hi, ' + user.first_name + ' ' + user.last_name + ' as you requested for your username here is your username ' + user.get_username()
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email, ]
    send_mail(subject, message, email_from, recipient_list)
    return redirect(reverse('get-user-name'))


class EmailUser(TemplateView):
    template_name = 'registration/get_user_name.html'


class EmailUserForm(TemplateView):
    template_name = 'registration/get_user_form.html'


def team(request, pk): #team wale page se yahan ayenge to jo team pe click krenge uska ayega data 
    user_sel = UserSelect.objects.filter(user=request.user, team=pk)
    batsmen = []
    bowlers = []
    all_players = []
    for i in user_sel:
        if i.batsman:
            batsmen.append(i.batsman)
            all_players.append(i.batsman)
        if i.bowler:
            bowlers.append(i.bowler)
            all_players.append(i.bowler)
    context = {
        'all_players': all_players,
        'batsmen': batsmen,
        'bowlers': bowlers,
    }
    return render(request, 'team_analysis.html', context)
