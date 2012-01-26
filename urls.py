from django.conf.urls.defaults import patterns, url, include
#from django.views.generic.simple import direct_to_template
#from clients.views import InscriptionWizard
#from clients.forms import Step1Form, Step2Form, Step3Form, Step4Form, Step5Form
from django.views.generic import UpdateView, DeleteView
from Instantaneus.magasins.models import Magasin
from Instantaneus.magasins.views import MagasinCreateView
from Instantaneus.magasins.models import MagasinForm
from Instantaneus.magasins.models import MagasinOwnerProfileForm
from django.contrib.auth.decorators import login_required
 


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^accounts/', include('registration.backends.default.urls')),
    #(r'^clients/api/(?P<email>[a-zA-Z0-9._%-+]+@[a-zA-Z0-9._%-]+.[a-zA-Z]{2,6})/$', 'clients.api.evenements_par_client'),
    #Clients
    (r'^clients/',include('Instantaneus.clients.urls')),
#    (r'^clients/api/(?P<email>[a-zA-Z0-9._%-+]+@[a-zA-Z0-9._%-]+.[a-zA-Z]{2,6})/$', 'clients.api.evenements_par_client'),
#    url(r'^clients/apropos/$',direct_to_template,{'template': 'clients/clients_apropos.html'},name='clients_apropos'),
#    url(r'^clients/intro/$',direct_to_template,{'template': 'clients/clients_intro.html'},name='intro_client'),
#    url(r'^clients/$', InscriptionWizard.as_view([Step1Form, Step2Form, Step3Form, Step4Form, Step5Form]), name='inscription_client'),
    #Evenements
    (r'^magasin/',include('Instantaneus.evenements.urls')),
#    (r'magasin/(?P<magasin_id>\d+)/evenement/new/$', login_required(EvenementCreateView.as_view(model=Evenement))),
#    url(r'magasin/(?P<magasin_id>\d+)/evenement/(?P<pk>\d+)/$', login_required(EvenementDetailView.as_view(model=Evenement)), name='evenement_details'),
#    url(r'magasin/(?P<magasin_id>\d+)/evenement/(?P<pk>\d+)/activer$', 'evenements.views.activation', name='evenement_activer'),
#    url(r'magasin/(?P<magasin_id>\d+)/evenement/(?P<pk>\d+)/supprimer$', login_required(EvenementDeleteView.as_view(model=Evenement, success_url="/magasin/liste")), name='evenement_supprimer'),
#    url(r"magasin/(?P<magasin_id>\d+)/evenement/(?P<pk>\d+)/modifier$", login_required(EvenementUpdateView.as_view(model=Evenement, form_class=EvenementForm)), name='evenement_modifier'),
    #Magasins
    url(r"magasin/ajouter/$", login_required(MagasinCreateView.as_view(model=Magasin, success_url="/magasin/liste")), name='magasin_ajouter'),
    url(r"magasin/(?P<pk>\d+)/modifier/$", login_required(UpdateView.as_view(model=Magasin, success_url="/magasin/liste", form_class=MagasinForm)), name='magasin_modifier'),
    url(r"magasin/(?P<pk>\d+)/supprimer/$", login_required(DeleteView.as_view(model=Magasin, success_url="/magasin/liste")), name='magasin_supprimer'),
    url(r'^magasin/liste/?$', 'magasins.views.user_magasins', name='user_magasins'),
    # FIN DES PATTERNS A NE PAS TOUCHER
    url(r'^owner_profil/$','magasins.views.redirectprofile',),
    ('^profiles/edit', 'profiles.views.edit_profile', {'form_class': MagasinOwnerProfileForm,}),
    (r'^profiles/', include('profiles.urls')),
                        )

from django.conf import settings

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^rosetta/', include('rosetta.urls')),
    )