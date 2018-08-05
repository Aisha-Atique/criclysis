from main.models import Team, UserSelect
from django.shortcuts import get_object_or_404


def picks(request):
    if request.user.is_authenticated():
        if Team.objects.filter(user=request.user).exists():
            team = get_object_or_404(Team, user=request.user)
            choices = {1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E'}
            all_picks = ''
            for i in range(team.total):
                all_picks += 'Team ' + choices[team.arr[i]] + ', '
            pick = choices[team.arr[team.counter]]
            total = team.total
            return {'pick': pick, 'all_picks': all_picks, 'total_teams': total}

        else:
            return {'pick': '', 'all_picks': '', 'total_teams': ''}
    return {'return': ''}


def total_check(request):
    if request.user.is_authenticated():
        if UserSelect.objects.filter(user=request.user).exists():
            all_select = UserSelect.objects.filter(user=request.user).count()
            team = get_object_or_404(Team, user=request.user)
            total = team.total * 2
            if all_select == total:
                info = "All Teams Created"
                return {'info': info}
        else:
            return {'info': ''}
    return {'return': ''}

