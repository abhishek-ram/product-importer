from django.views.generic import TemplateView


class IndexView(TemplateView):
    """ View for the default index page"""
    template_name = 'index.html'

