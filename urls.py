from django.conf.urls import url

# We can't import the theme module directly because it has a hyphen in its name. This works well.
import importlib
theme_views = importlib.import_module('presupuesto-navarra.views')

# We can define additional URLs applicable only to the theme. These will get added
# to the project URL patterns list.
EXTRA_URLS = (
    url(r'^visita-guiada$', theme_views.guidedvisit, name='guidedvisit'),
    url(r'^covid$', theme_views.covid, name='covid'),
)
