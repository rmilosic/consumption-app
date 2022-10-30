from curses.ascii import HT
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views import View
from .forms import LoginForm

from django.contrib.auth import authenticate



class LoginView(View):
    # form_class = MyForm
    # initial = {'key': 'value'}
    template_name = 'base_login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            
            # redirect()
            # TODO: redirect depending on user role
            return render(request, self.template_name, {"form": form})
        else:
            form = LoginForm()
            # form = self.form_class(initial=self.initial)
            return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        
        form = LoginForm(request.POST)
        
        if form.is_valid():
        
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            
            # authenticate            
            user = authenticate(username=username, password=password)

            # TODO: define responses
            if user is not None:
                # A backend authenticated the credentials
                return HttpResponse('logged in')
            else:
                # No backend authenticated the credentials
                # <process form cleaned data>
                return HttpResponse('not logged in')

        else:
            return HttpResponse("form not valid")
        # return render(request, self.template_name, {'form': form})
    
class UsersBulkImportView(View):
    # form_class = MyForm
    # initial = {'key': 'value'}
    # template_name = 'form_template.html'

    def get(self, request, *args, **kwargs):
        # form = self.form_class(initial=self.initial)
        # return render(request, self.template_name, {'form': form})
        return HttpResponse("Uvoz uporabnikov")
    
    
class ConsumptionBulkImportView(View):
    # form_class = MyForm
    # initial = {'key': 'value'}
    # template_name = 'form_template.html'

    def get(self, request, *args, **kwargs):
        # form = self.form_class(initial=self.initial)
        # return render(request, self.template_name, {'form': form})
        return HttpResponse("Uvoz porabe")



class UserView(View):
    # form_class = MyForm
    # initial = {'key': 'value'}
    # template_name = 'form_template.html'

    def get(self, request, *args, **kwargs):
        # form = self.form_class(initial=self.initial)
        # return render(request, self.template_name, {'form': form})
        return HttpResponse("Uporabnik")
    
    
class ConsumptionView(View):
    # form_class = MyForm
    # initial = {'key': 'value'}
    # template_name = 'form_template.html'

    def get(self, request, *args, **kwargs):
        # form = self.form_class(initial=self.initial)
        # return render(request, self.template_name, {'form': form})
        return HttpResponse("Poraba")
    
    
class AdministratorView(View):
    # form_class = MyForm
    # initial = {'key': 'value'}
    # template_name = 'form_template.html'

    def get(self, request, *args, **kwargs):
        # form = self.form_class(initial=self.initial)
        # return render(request, self.template_name, {'form': form})
        return HttpResponse("Administrator")