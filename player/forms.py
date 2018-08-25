from django import forms
from .models import Bowlers
from crispy_forms.helper import FormHelper
from .choices import *


class BowlerListFormHelper(FormHelper):
    model = Bowlers
    form_tag = False
    form_class = 'form-horizontal'
    field_class = 'col-lg-8'
    label_class = 'col-lg-2'
    Playing_role = forms.ChoiceField(choices=ROLE_CHOICES, required=True)
