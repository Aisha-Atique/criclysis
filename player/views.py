
from .tables import BowlerTable
from .filters import BowlerListFilter
from .utils import PagedFilteredTableView
from .models import Bowlers
from .forms import BowlerListFormHelper
from django.contrib.auth.mixins import LoginRequiredMixin
from main.models import UserSelect
from django.shortcuts import render


class BowlerList(LoginRequiredMixin, PagedFilteredTableView):
    model = Bowlers
    template_name = 'bowlers_list.html'
    table_class = BowlerTable
    filter_class = BowlerListFilter
    formhelper_class = BowlerListFormHelper

    def get_context_data(self, **kwargs):
        context = super(BowlerList, self).get_context_data(**kwargs)
        context['select_list'] = UserSelect.objects.filter(user=self.request.user)
        return context
