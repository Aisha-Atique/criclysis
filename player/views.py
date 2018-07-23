
from .tables import BowlerTable
from .filters import BowlerListFilter
from .utils import PagedFilteredTableView
from .models import Bowlers
from .forms import BowlerListFormHelper
from django.shortcuts import render


class BowlerList(PagedFilteredTableView):
    model = Bowlers
    template_name = 'bowlers_list.html'
    table_class = BowlerTable
    filter_class = BowlerListFilter
    formhelper_class = BowlerListFormHelper
