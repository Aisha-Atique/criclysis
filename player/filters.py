import django_filters as df
from .models import Bowlers


class BowlerListFilter(df.FilterSet):
    class Meta:
        model = Bowlers
        fields = ['name', 'Playing_Role']

