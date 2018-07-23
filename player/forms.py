from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from crispy_forms.bootstrap import InlineField, FormActions, StrictButton
from crispy_forms.layout import Layout
from .models import Bowlers


# class BowlerListFormHelper(FormHelper):
#     form_id = 'bowler-search-form'
#     form_class = 'form-inline'
#     field_template = 'bootstrap3/layout/inline_field.html'
#     field_class = 'col-xs-3'
#     label_class = 'col-xs-3'
#     form_show_errors = True
#     help_text_inline = False
#     html5_required = True
#     form_tag = False
#     layout = Layout(
#                 Fieldset(
#                     '<i class="fa fa-search"></i> Search Bowler Records',
#                     InlineField('name'),
#                     InlineField('ahprank'),
#                     InlineField('pcarank'),
#                 ),
#                 FormActions(
#                     StrictButton(
#                         '<i class="fa fa-search"></i> Search',
#                         type='submit',
#                         css_class='btn-primary',
#                         style='margin-top:10px;')
#                 )
#     )
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
