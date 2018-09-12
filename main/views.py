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
        context = {
            'bowler': bowler,
            'select_list': select_list,
            'all_select': all_select,
            'team': team,
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


def team(request, pk):
    if not request.user.is_authenticated():
        return render(request, 'registration/login.html')
    else:
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

        dataSource = {}
        dataSource['chart'] = {
            "caption": "Team Ahp Rank",
            "subCaption": "For all selected Batsmen",
            "xAxisName": "Names",
            "yAxisName": "Ahp Rank",
            # "numberPrefix": "$",
            "theme": "zune",
            "type": "column2D"
        }

        dataSource['data'] = []
        # Iterate through the data in `Revenue` model and insert in to the `dataSource['data']` list.
        for key in batsmen:
            data = {}
            data['label'] = key.name
            data['value'] = key.ahprank

            dataSource['data'].append(data)

        column2D = FusionCharts("column2D", "ex1", "600", "350", "chart-1", "json", dataSource)

        dataSource2 = {}
        dataSource2['chart'] = {
            "caption": "Team PCA Rank",
            "subCaption": "For all selected Batsmen",
            "xAxisName": "Names",
            "yAxisName": "PCA Rank",
            # "numberPrefix": "$",
            "theme": "zune",
            "type": "column2D"
        }

        dataSource2['data'] = []

        for key in batsmen:
            data = {}
            data['label'] = key.name
            data['value'] = key.rank

            dataSource2['data'].append(data)

        # Create an object for the Column 2D chart using the FusionCharts class constructor
        column = FusionCharts("column2D", "ex2", "600", "350", "chart-2", "json", dataSource2)

        dataSource3 = {}
        dataSource3['chart'] = {
            "caption": "Team Batting Strike-Rate",
            "subCaption": "For all selected Batsmen",
            "xAxisName": "Names",
            "yAxisName": "Strike-Rate",
            # "numberPrefix": "$",
            "theme": "zune",
            "type": "column2D"
        }

        dataSource3['data'] = []

        for key in batsmen:
            data = {}
            data['label'] = key.name
            data['value'] = key.sr

            dataSource3['data'].append(data)

        # Create an object for the Column 2D chart using the FusionCharts class constructor
        column3 = FusionCharts("column2D", "ex3", "600", "350", "chart-3", "json", dataSource3)

        batsmenaverage = {}
        batsmenaverage['chart'] = {
            "caption": "Team Batting Average",
            "subCaption": "For all selected Batsmen",
            "xAxisName": "Names",
            "yAxisName": "Average",
            # "numberPrefix": "$",
            "theme": "zune",
            "type": "column2D"
        }

        batsmenaverage['data'] = []

        for key in batsmen:
            data = {}
            data['label'] = key.name
            data['value'] = key.ave

            batsmenaverage['data'].append(data)

        # Create an object for the Column 2D chart using the FusionCharts class constructor
        column4 = FusionCharts("column2D", "ex4", "600", "350", "chart-4", "json", batsmenaverage)

        batsmenconsistent = {}
        batsmenconsistent['chart'] = {
            "caption": "Team Batting Average",
            "subCaption": "For all selected Batsmen",
            "xAxisName": "Names",
            "yAxisName": "Average",
            # "numberPrefix": "$",
            "theme": "zune",
            "type": "column2D"
        }

        batsmenconsistent['data'] = []

        for key in batsmen:
            data = {}
            data['label'] = key.name
            data[
                'value'] = key.ave * 0.4262 + key.inningsplayed * 0.2566 + key.sr * 0.1510 + key.fifty * 0.0556 + key.centuries * 0.0787 - key.zeros * 0.0328

            batsmenconsistent['data'].append(data)

        # Create an object for the Column 2D chart using the FusionCharts class constructor
        column5 = FusionCharts("column2D", "ex5", "600", "350", "chart-5", "json", batsmenconsistent)

        batsmenhitter = {}
        batsmenhitter['chart'] = {
            "caption": "Team Batting Hard Hitters",
            "subCaption": "For all selected Batsmen",
            "xAxisName": "Names",
            "yAxisName": "Hard-Hitter",
            # "numberPrefix": "$",
            "theme": "zune",
            "type": "column2D"
        }

        batsmenhitter['data'] = []

        for key in batsmen:
            data = {}
            data['label'] = key.name
            data['value'] = key.hardhitter

            batsmenhitter['data'].append(data)

        # Create an object for the Column 2D chart using the FusionCharts class constructor
        column7 = FusionCharts("column2D", "ex7", "600", "350", "chart-7", "json", batsmenhitter)

        batsmendotball = {}
        batsmendotball['chart'] = {
            "caption": "Team Batting Dot Balls View",
            "subCaption": "For all selected Batsmen",
            "xAxisName": "Names",
            "yAxisName": "Dot balls ratio",
            # "numberPrefix": "$",
            "theme": "zune",
            "type": "column2D"
        }

        batsmendotball['data'] = []

        for key in batsmen:
            data = {}
            data['label'] = key.name
            data['value'] = key.dotball

            batsmendotball['data'].append(data)

        # Create an object for the Column 2D chart using the FusionCharts class constructor
        column8 = FusionCharts("column2D", "ex8", "600", "350", "chart-8", "json", batsmendotball)

        # bowler charts started

        Source = {}
        Source['chart'] = {
            "caption": "Team Ahp Rank",
            "subCaption": "For all selected Bowler",
            "xAxisName": "Names",
            "yAxisName": "Ahp Rank",
            # "numberPrefix": "$",
            "theme": "zune",
            "type": "column2D"
        }

        Source['data'] = []
        # Iterate through the data in `Revenue` model and insert in to the `dataSource['data']` list.
        for key in bowlers:
            data = {}
            data['label'] = key.name
            data['value'] = key.ahprank

            Source['data'].append(data)

        column9 = FusionCharts("column2D", "ex9", "600", "350", "chart-9", "json", Source)

        Source2 = {}
        Source2['chart'] = {
            "caption": "Team PCA Rank",
            "subCaption": "For all selected Bowler",
            "xAxisName": "Names",
            "yAxisName": "PCA Rank",
            # "numberPrefix": "$",
            "theme": "zune",
            "type": "column2D"
        }

        Source2['data'] = []

        for key in bowlers:
            data = {}
            data['label'] = key.name
            data['value'] = key.rank

            Source2['data'].append(data)

        # Create an object for the Column 2D chart using the FusionCharts class constructor
        column10 = FusionCharts("column2D", "ex10", "600", "350", "chart-10", "json", Source2)

        Source3 = {}
        Source3['chart'] = {
            "caption": "Team Bowling Strike-Rate",
            "subCaption": "For all selected Bowler",
            "xAxisName": "Names",
            "yAxisName": "Strike-Rate",
            # "numberPrefix": "$",
            "theme": "zune",
            "type": "column2D"
        }

        Source3['data'] = []

        for key in bowlers:
            data = {}
            data['label'] = key.name
            data['value'] = key.sr

            Source3['data'].append(data)

        # Create an object for the Column 2D chart using the FusionCharts class constructor
        column11 = FusionCharts("column2D", "ex11", "600", "350", "chart-11", "json", Source3)

        bowleraverage = {}
        bowleraverage['chart'] = {
            "caption": "Team Bowling Average",
            "subCaption": "For all selected Bowler",
            "xAxisName": "Names",
            "yAxisName": "Average",
            # "numberPrefix": "$",
            "theme": "zune",
            "type": "column2D"
        }

        bowleraverage['data'] = []

        for key in bowlers:
            data = {}
            data['label'] = key.name
            data['value'] = key.ave

            bowleraverage['data'].append(data)

        # Create an object for the Column 2D chart using the FusionCharts class constructor
        column12 = FusionCharts("column2D", "ex12", "600", "350", "chart-12", "json", bowleraverage)

        bowlerconsistent = {}
        bowlerconsistent['chart'] = {
            "caption": "Team Bowling Consistent Form",
            "subCaption": "For all selected Bowler",
            "xAxisName": "Names",
            "yAxisName": "Current Form metric",
            # "numberPrefix": "$",
            "theme": "zune",
            "type": "column2D"
        }

        bowlerconsistent['data'] = []

        for key in bowlers:
            data = {}
            data['label'] = key.name
            data[
                'value'] = key.totalovers * 0.3269 + key.matches * 0.2846 + key.sr * 0.1877 + key.ave * 0.1210 + key.wickettaker * 0.0798

            bowlerconsistent['data'].append(data)

        # Create an object for the Column 2D chart using the FusionCharts class constructor
        column13 = FusionCharts("column2D", "ex13", "600", "350", "chart-13", "json", bowlerconsistent)

        bowlerecon = {}
        bowlerecon['chart'] = {
            "caption": "Team Bowling Hard Hitters",
            "subCaption": "For all selected Bowler",
            "xAxisName": "Names",
            "yAxisName": "Economy",
            # "numberPrefix": "$",
            "theme": "zune",
            "type": "column2D"
        }

        bowlerecon['data'] = []

        for key in bowlers:
            data = {}
            data['label'] = key.name
            data['value'] = key.econ

            bowlerecon['data'].append(data)

        # Create an object for the Column 2D chart using the FusionCharts class constructor
        column14 = FusionCharts("column2D", "ex14", "600", "350", "chart-14", "json", bowlerecon)

        bowlerwkt = {}
        bowlerwkt['chart'] = {
            "caption": "Team Bowling Wicket Taking View",
            "subCaption": "For all selected Bowler",
            "xAxisName": "Names",
            "yAxisName": "Wickets ratio",
            # "numberPrefix": "$",
            "theme": "zune",
            "type": "column2D"
        }

        bowlerwkt['data'] = []

        for key in bowlers:
            data = {}
            data['label'] = key.name
            data['value'] = key.wickettaker

            bowlerwkt['data'].append(data)

        # Create an object for the Column 2D chart using the FusionCharts class constructor
        column15 = FusionCharts("column2D", "ex15", "600", "350", "chart-15", "json", bowlerwkt)

        context = {
            'all_players': all_players,
            'batsmen': batsmen,
            'bowlers': bowlers,
            'output': column2D.render(),
            'output2': column.render(),
            'output5': column5.render(),
            'output3': column3.render(),
            'output4': column4.render(),
            'output7': column7.render(),
            'output8': column8.render(),
            'output9': column9.render(),
            'output10': column10.render(),
            'output11': column11.render(),
            'output12': column12.render(),
            'output13': column13.render(),
            'output14': column14.render(),
            'output15': column15.render(),
        }
        return render(request, 'team_analysis.html', context)



