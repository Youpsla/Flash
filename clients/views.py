# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.contrib.formwizard.views import SessionWizardView
from Instantaneus.clients.models import Customer


class InscriptionWizard(SessionWizardView):
    
    def get_template_names(self):
        return 'clients/session_wizard.html'
    
    def done(self, form_list, **kwargs):
        instance = Customer()
        for form in form_list:
            for field, value in form.cleaned_data.iteritems():
                if field != 'category':
                    setattr(instance, field, value)
                else:
                    instance.save()
                    setattr(instance, field, value)
                    instance.save()
        return render_to_response('clients/index.html', {
            'form_data': [form.cleaned_data for form in form_list],
        })
    

    
        