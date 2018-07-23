import django_tables2 as tables
from django_tables2.utils import A
from .models import Bowlers
import django_tables2 as dt2


# class BowlerTable(dt2.Table):
# #     #name = tables.LinkColumn('customer-detail', args=[A('pk')])
# #    # ahprank = tables.LinkColumn('customer-detail', args=[A('pk')])
# #     #pcarank = tables.LinkColumn('customer-detail', args=[A('pk')])
# #     #customer_email = tables.LinkColumn('customer-detail', args=[A('pk')])
#     class Meta:
#         model = Bowlers
#         fields = ('name', 'ahprank', 'pcarank')
#         attrs = {"class": "table-striped table-bordered"}
#         empty_text = "There are no customers matching the search criteria..."


class BowlerTable(dt2.Table):
    name = tables.LinkColumn('BowlerDetailView', args=[A('pk')])
    # ahprank = tables.LinkColumn('BowlerList', args=[A('pk')])
    # pcarank = tables.LinkColumn('BowlerList', args=[A('pk')])
    class Meta:
                model = Bowlers
                fields = ('name', 'ahprank', 'pcarank')
                template_name = 'django_tables2/bootstrap-responsive.html'
                #attrs = {"class": "paleblue"}
                attrs = {'class': 'table table-striped table-bordered table-hover'}
                per_page = 10
