from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from clients.views import InscriptionWizard
from clients.forms import Step1Form, Step2Form, Step3Form, Step4Form, Step5Form
from django.contrib.sites.models import Site
from django.views.generic import DetailView
from django.views.generic import UpdateView, DeleteView
from magasins.models import Magasin
from magasins.views import MagasinCreateView
from magasins.models import MagasinForm
from evenements.models import Evenement
from evenements.views import EvenementCreateView, EvenementUpdateView
from evenements.forms import EvenementForm
 


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^clients/$', InscriptionWizard.as_view([Step1Form, Step2Form, Step3Form, Step4Form, Step5Form])),
    (r'^accounts/', include('registration.backends.default.urls')),
    (r'magasin/(?P<magasin_id>\d+)/evenement/new/$', EvenementCreateView.as_view(model=Evenement)),
    url(r'magasin/(?P<magasin_id>\d+)/evenement/(?P<pk>\d+)/$', DetailView.as_view(model=Evenement), name='evenement_details'),
    url(r'magasin/(?P<magasin_id>\d+)/evenement/(?P<pk>\d+)/activer$', 'evenements.views.activation', name='evenement_activer'),
    url(r'magasin/(?P<magasin_id>\d+)/evenement/(?P<pk>\d+)/supprimer$', DeleteView.as_view(model=Evenement, success_url="/magasin/liste"), name='evenement_supprimer'),
    url(r"magasin/ajouter/$", MagasinCreateView.as_view(model=Magasin, success_url="/magasin/liste"), name='magasin_ajouter'),
    url(r"magasin/(?P<magasin_id>\d+)/evenement/(?P<pk>\d+)/modifier$", EvenementUpdateView.as_view(model=Evenement, form_class=EvenementForm), name='evenement_modifier'),
    url(r"magasin/(?P<pk>\d+)/modifier/$", UpdateView.as_view(model=Magasin, success_url="/magasin/liste", form_class=MagasinForm), name='magasin_modifier'),
    url(r"magasin/(?P<pk>\d+)/supprimer/$", DeleteView.as_view(model=Magasin, success_url="/magasin/liste"), name='magasin_supprimer'),
    url(r'^magasin/liste/?$', 'magasins.views.user_magasins', name='user_magasins'),
    # FIN DES PATTERNS A NE PAS TOUCHER
    url(r'^magasin/$',
        direct_to_template,
        {'template': 'magasins/home_shop.html',}, name='magasin',),
    url(r'^owner_profil/$','magasins.views.redirectprofile',),
    (r'^profiles/', include('profiles.urls')),
#    url(r'^magasin/$',
#        direct_to_template,
#        {'template': 'magasins/magasin_base.html', 'extra_context' : {'nom_site' : Site.objects.get_current()}},
#        name='index',),  
)
from django.conf import settings

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^rosetta/', include('rosetta.urls')),
    )