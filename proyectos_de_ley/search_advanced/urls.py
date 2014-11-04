from django.conf.urls import patterns, url

from .forms import SearchAdvancedForm
from .views import SearchWizard


urlpatterns = patterns(
    '',
    url(r'^$', SearchWizard.as_view([SearchAdvancedForm])),
)