# -*- coding: UTF-8 -*-

from django.conf.urls import patterns, url

MAIN_ENTITY_LEVEL = 'comunidad'
MAIN_ENTITY_NAME = 'Navarra'

BUDGET_LOADER = 'NavarraBudgetLoader'

FEATURED_PROGRAMMES = ['3123', '2315', '1321', '3341']

OVERVIEW_INCOME_NODES = [
                          {
                            'nodes': [['10', '100']],
                            'label.es': 'Impuesto sobre la renta de las personas físicas',
                            'label.eu': 'Impuesto sobre la renta de las personas físicas',
                            'link_id': '10'
                          },
                          '21',
                          {
                            'nodes': [['22', '220']],
                            'label.es': 'Impuestos especiales',
                            'label.eu': 'Impuestos especiales',
                            'link_id': '22'
                          },
                          {
                            'nodes': [['10', '101']],
                            'label.es': 'Impuesto sobre sociedades',
                            'label.eu': 'Impuesto sobre sociedades',
                            'link_id': '10'
                          },
                        ]
OVERVIEW_EXPENSE_NODES = [ '31', '32', '94', '23', '45', '95', '21' ]

# How aggresive should the Sankey diagram reorder the nodes. Default: 0.79 (Optional)
# Note: 0.5 usually leaves nodes ordered as defined. 0.95 sorts by size (decreasing).
OVERVIEW_RELAX_FACTOR = 0.4

# Treemaps minimum height or width to show labels. Default: 70 (Optional)
TREEMAP_LABELS_MIN_SIZE = 50

# Show Payments section in menu & home options. Default: False.
# SHOW_PAYMENTS           = True

# Show Tax Receipt section in menu & home options. Default: False.
SHOW_TAX_RECEIPT        = True

# Show Counties & Towns links in Policies section in menu & home options. Default: False.
# SHOW_COUNTIES_AND_TOWNS = False

# Show an extra tab with institutional breakdown. Default: True.
SHOW_INSTITUTIONAL_TAB  = False

# Show an extra tab with funding breakdown (only applicable to some budgets). Default: False.
# SHOW_FUNDING_TAB = False

# Adjust inflation in amounts in Overview page. Default: True
ADJUST_INFLATION_IN_OVERVIEW = False

# Show Subtotals panel in Overview. Default: False
# SHOW_OVERVIEW_SUBTOTALS = True

# Calculate budget indicators (True), or show/hide the ones hardcoded in HTML (False). Default: True.
# CALCULATE_BUDGET_INDICATORS = False

# Show an extra column with actual revenues/expenses. Default: True.
# Warning: the execution data still gets shown in the summary chart and in downloads.
#SHOW_ACTUAL = True

# Should we group elements at the economic subheading level, or list all of them,
# grouping by uid?. Default: True. (i.e. group by uid, show all elements)
BREAKDOWN_BY_UID = False

# Include financial income/expenditures in overview and global policy breakdowns. Default: False.
INCLUDE_FINANCIAL_CHAPTERS_IN_BREAKDOWNS = False

# Search in entity names. Default: True.
SEARCH_ENTITIES = False

# Supported languages. Default: ('es', 'Castellano')
LANGUAGES = (
  ('es', 'Castellano'),
  ('eu', 'Euskera'),
)

# Facebook Aplication ID used in social_sharing temaplate. Default: ''
# In order to get the ID create an app in https://developers.facebook.com/
FACEBOOK_ID             = '238494156568926'

# Google Analytics ID. Default: ''
# In order to get the ID create a Google Analytics Acount in https://analytics.google.com/analytics/web/
ANALYTICS_ID            = 'UA-28946840-17'

# Setup Data Source Budget link
DATA_SOURCE_BUDGET      = 'http://www.gobiernoabierto.navarra.es/es/open-data/datos/etiquetas/228'

# Setup Data Source Population link
DATA_SOURCE_POPULATION  = 'http://www.navarra.es/AppsExt/GN.InstitutoEstadistica.Web/consulta.aspx?TC=1'

# Setup Data Source Inflation link
DATA_SOURCE_INFLATION   = 'http://www.navarra.es/AppsExt/GN.InstitutoEstadistica.Web/informacionestadistica.aspx?R=1&E=1'

# Setup Main Entity Web Url
MAIN_ENTITY_WEB_URL     = 'http://www.navarra.es/home_es/Navarra/'

# Setup Main Entity Legal Url (if empty we hide the link)
MAIN_ENTITY_LEGAL_URL   = 'http://www.navarra.es/home_es/Aviso/avisoLegal.htm'

# External URL for Cookies Policy (if empty we use out template page/cookies.html)
#COOKIES_URL             = 'http://www.santiagodecompostela.gal/avisolegal.php?lg=gal'

# Allow overriding of default treemap color scheme
# COLOR_SCALE = [ '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#e7969c', '#bcbd22', '#17becf' ]
