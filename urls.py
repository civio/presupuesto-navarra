from django.conf.urls import url

# We can define additional URLs applicable only to the theme. These will get added
# to the project URL patterns list.
EXTRA_URLS = (
    url(r'^visita-guiada$', 'guidedvisit', name='guidedvisit'),
    url(r'^covid$', 'covid', name='covid'),
)
