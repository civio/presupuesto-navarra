# -*- coding: UTF-8 -*-

from budget_app.models import BudgetBreakdown, Entity, EconomicCategory
from budget_app.views.helpers import *

def covid(request, render_callback=None):
    c = get_context(request, css_class='body-entities', title='')
    entity = get_main_entity(c)

    # Prepare the budget breakdowns
    c['breakdowns'] = {
        'financial_expense': BudgetBreakdown(),
        'functional': BudgetBreakdown(['policy', 'programme', get_final_element_grouping(c)]),
        'institutional': get_institutional_breakdown(c) if c['show_global_institutional_treemap'] else None
    }

    c['breakdowns']['economic'] = BudgetBreakdown(['article', 'heading'])

    # Ignore if possible the descriptions for execution data, they are truncated and ugly
    programme_descriptions = {}
    def _populate_programme_descriptions(column_name, item):
        item_uid = getattr(item, get_final_element_grouping(c))()
        if not item.actual or not item_uid in programme_descriptions:
            programme_descriptions[item_uid] = getattr(item, 'description')

    # We assume here that all items are properly configured across all dimensions
    # (and why wouldn't they? see below). Note that this is a particular case of the
    # more complex logic below for small entities, and I used for a while the more 
    # general code for all scenarios, until I realised performance was much worse,
    # as we do two expensive denormalize-the-whole-db queries!
    get_budget_breakdown(   "e.id = %s AND b.year = '2020' AND i.description LIKE %s", [ entity.id, 'COVID%' ],
                            [ 
                                c['breakdowns']['economic'],
                                c['breakdowns']['functional'],
                                c['breakdowns']['institutional']
                            ],
                            _populate_programme_descriptions )

    # Additional data needed by the view
    populate_level(c, entity.level)
    populate_entity_stats(c, entity)
    # TODO: We're doing this also for Aragon, check performance!
    populate_entity_descriptions(c, entity)

    # We do some convoluted stuff (copied from programmes code) to show item-level descriptions
    # in the functional breakdown
    c['descriptions'] = Budget.objects.get_all_descriptions(entity).copy()
    programme_descriptions.update(c['descriptions']['functional'])
    c['descriptions']['functional'] = programme_descriptions

    populate_years(c, c['breakdowns']['economic'])
    populate_budget_statuses(c, entity.id)
    populate_area_descriptions(c, ['functional', 'income', 'expense', 'institutional'])
    set_full_breakdown(c, entity.level == settings.MAIN_ENTITY_LEVEL)
    c['entity'] = entity

    # XXX
    c['budget_statuses']='{"2020": ""}'
    c['show_actual']=False

    # if parameter widget defined use policies/widget template instead of policies/show
    template = 'covid/show_widget.html' if isWidget(request) else 'covid/show.html'

    return render(c, render_callback, template)
