from curses.ascii import HT
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.utils import IntegrityError

from django.shortcuts import redirect, render
from django.views import View
from django.template.loader import get_template

from django.contrib.auth import authenticate, login, logout

from .forms import LoginForm, UploadUsersFromFileForm
from .decorators import *

from .handlers import handle_file_upload_import_users

class IndexView(View):
    # redirect depending on user group
    def get(self, request, *args, **kwargs):
        
        if request.user.groups.filter(name='admin').exists():
        # Action if existing
            # navigate to admin dashboard
            return redirect("backend:administrator")
        else:
            # Action if not existing
            return redirect("backend:user")


class LoginView(View):
    # form_class = MyForm
    # initial = {'key': 'value'}
    template_name = 'base_login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:

            return redirect("backend:index")
        
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

            if user is not None:
                # A backend authenticated the credentials
                login(request, user)
                return redirect("backend:index")
            else:
                # No backend authenticated the credentials
                # <process form cleaned data>
                messages.error(request,'username or password not correct')
                return redirect("backend:login")

        else:
            
            return redirect("backend:login")


class LogoutView(View):
    def post(self, request, *args, **kwargs):
        logout(request)        
        return redirect("backend:login")


class UsersBulkImportView(UserPassesTestMixin, View):
    # form_class = MyForm
    # initial = {'key': 'value'}
    template_name = 'base_usersBulkImport.html'

    def get(self, request, *args, **kwargs):
        # form = self.form_class(initial=self.initial)
        # return render(request, self.template_name, {'form': form})
        form = UploadUsersFromFileForm()
        return render(request, self.template_name, {"form": form})
    
    def post(self, request, *args, **kwargs):
        form = UploadUsersFromFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                res = handle_file_upload_import_users(request.FILES['file'])
                messages.success(request, res)
                return render(request, self.template_name, {"form": form})
            except IntegrityError as e:
            # show success message
                messages.error(request, str(e.__cause__))
                return render(request, self.template_name, {"form": form})
                
        else:
            form = UploadUsersFromFileForm()
            # show error message
        return render(request, self.template_name, {"form": form})
        
    def test_func(self):
        return is_admin(self.request.user)

    
class ConsumptionBulkImportView(View):
    # form_class = MyForm
    # initial = {'key': 'value'}
    template_name = 'base_usersBulkImport.html'

    def get(self, request, *args, **kwargs):
        # form = self.form_class(initial=self.initial)
        # return render(request, self.template_name, {'form': form})
         return render(request, self.template_name)
    
    def post(self, request, *args, **kwargs):
        pass



class UserView(View):
    # form_class = MyForm
    # initial = {'key': 'value'}
    template_name = 'base_user.html'

    def get(self, request, *args, **kwargs):
        # form = self.form_class(initial=self.initial)
        return render(request, self.template_name)
        
    
    
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
    template_name = 'base_admin.html'

    def get(self, request, *args, **kwargs):
        # form = self.form_class(initial=self.initial)
        # return render(request, self.template_name, {'form': form})
        return render(request, self.template_name)