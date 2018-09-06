import django_tables2 as tables
from django_tables2.utils import A
from .models import Bowlers, Batsmen
import django_tables2 as dt2


class BowlerTable(dt2.Table):
    name = tables.LinkColumn('bowler-detail', args=[A('pk')])
    wkts = tables.Column(visible=False)

    class Meta:
                model = Bowlers
                fields = ('name', 'role', 'ahprank')
                template_name = 'django_tables2/bootstrap-responsive.html'
                attrs = {'class': 'table table-striped table-bordered table-hover'}
                per_page = 10
                order_by = 'ahprank'


class BowlerTablePCA(dt2.Table):
    name = tables.LinkColumn('bowler-detail', args=[A('pk')])
    wkts = tables.Column(visible=False)

    class Meta:
                model = Bowlers
                fields = ('name', 'role', 'rank')
                template_name = 'django_tables2/bootstrap-responsive.html'
                attrs = {'class': 'table table-striped table-bordered table-hover'}
                per_page = 10
                order_by = 'pcarank'


class BatsmenTablePCA(dt2.Table):
    name = tables.LinkColumn('batsman-detail', args=[A('pk')])
    hardhitter = tables.Column(visible=False)
    finisher = tables.Column(visible=False)
    fifty = tables.Column(visible=False)

    class Meta:
                model = Batsmen
                fields = ('name', 'role', 'rank')
                template_name = 'django_tables2/bootstrap-responsive.html'
                attrs = {'class': 'table table-striped table-bordered table-hover'}
                per_page = 10
                order_by = 'pcarank'


class BatsmenTableAHP(dt2.Table):
    name = tables.LinkColumn('batsman-detail', args=[A('pk')])
    hardhitter = tables.Column(visible=False)
    finisher = tables.Column(visible=False)
    fifty = tables.Column(visible=False)


    class Meta:
                model = Batsmen
                fields = ('name', 'role', 'ahprank')
                template_name = 'django_tables2/bootstrap-responsive.html'
                attrs = {'class': 'table table-striped table-bordered table-hover'}
                per_page = 10
                order_by = 'ahprank'
