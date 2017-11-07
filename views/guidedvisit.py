# -*- coding: UTF-8 -*-
from coffin.shortcuts import render_to_response
from budget_app.views.helpers import *

def guidedvisit(request, render_callback=None):
    # Get request context
    c = get_context(request, css_class='body-entities', title='')

    # Setup active_tab for menu options
    c['active_tab'] = 'guidedvisit'

    return render_to_response('guidedvisit/index.html', c)
