from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

#class IndexView(LoginRequiredMixin, TemplateView):
#    template_name = 'docs_work/post_list.html'
    
#    def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs)
#        context['is_author'] = self.request.user.groups.filter(name = 'authors').exists()
#        return context    

from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from .models import BaseRegisterForm

class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
#    success_url = '/users/upgrade/'
    
#    def get_success_url(self):
#        return redirect('/users')

#    def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs)
#        context['is_not_author'] = not self.request.user.groups.filter(name = 'authors').exists()
#        return context 



@login_required
def upgrade_me(request):
    user = request.user
    author_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        author_group.user_set.add(user)
    return redirect('/docs_work')

@login_required
def common_me(request):
    user = request.user
    author_group = Group.objects.get(name='common')
    if not request.user.groups.filter(name='common').exists():
        author_group.user_set.add(user)
    return redirect('/docs_work')





