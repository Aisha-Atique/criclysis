
from .tables import BowlerTable, BowlerTablePCA, BatsmenTablePCA, BatsmenTableAHP
from .filters import BowlerListFilter
from .utils import PagedFilteredTableView
from .models import Bowlers, Batsmen
from .forms import BowlerListFormHelper
from django.contrib.auth.mixins import LoginRequiredMixin


class BowlerList(LoginRequiredMixin, PagedFilteredTableView):
    model = Bowlers
    template_name = 'bowlers_list.html'
    table_class = BowlerTable
    filter_class = BowlerListFilter
    formhelper_class = BowlerListFormHelper


class BowlerListPCA(LoginRequiredMixin, PagedFilteredTableView):
    model = Bowlers
    template_name = 'pca.html'
    table_class = BowlerTablePCA
    filter_class = BowlerListFilter
    formhelper_class = BowlerListFormHelper


class BatsmanListPCA(LoginRequiredMixin, PagedFilteredTableView):
    model = Batsmen
    template_name = 'pca_batsman.html'
    table_class = BatsmenTablePCA
    filter_class = BowlerListFilter
    formhelper_class = BowlerListFormHelper


class BatsmanListAHP(LoginRequiredMixin, PagedFilteredTableView):
    model = Batsmen
    template_name = 'ahp_batsman.html'
    table_class = BatsmenTableAHP
    filter_class = BowlerListFilter
    formhelper_class = BowlerListFormHelper


