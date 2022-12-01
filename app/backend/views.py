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

from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

from django.conf import settings

from .forms import LoginForm, UploadUsersFromFileForm, UploadConsumptionReportForm
from .decorators import *
from .models import Building, Apartment, ConsumptionReport

from .handlers import handle_file_upload_import_users, handle_file_upload_import_consumption

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
    template_name = 'base_consumptionBulkImport.html'

    def get(self, request, *args, **kwargs):
        form = UploadConsumptionReportForm()
        # return render(request, self.template_name, {'form': form})
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = UploadConsumptionReportForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                season = form.cleaned_data["season"]
                month = form.cleaned_data["month"]
                res = handle_file_upload_import_consumption(request.FILES['file'], month=month, season=season)
                messages.success(request, res)
                return render(request, self.template_name, {"form": form})
            except IntegrityError as e:
            # show success message
                messages.error(request, str(e.__cause__))
                return render(request, self.template_name, {"form": form})
                    
        else:
            return render(request, self.template_name, {"form": form})

    def test_func(self):
        return is_admin(self.request.user)
    


class UserView(View):
    # form_class = MyForm
    # initial = {'key': 'value'}
    template_name = 'base_user.html'

    def get(self, request, *args, **kwargs):
        # form = self.form_class(initial=self.initial)
        
        month = request.GET.get("month", None)
        season = request.GET.get("season", None)
        print("month", month)
        
        # get apartment
        apartment = Apartment.objects.get(owner_id=request.user.id)
        
        
        # get all apt reports  
        consumption_apartment_all = ConsumptionReport.objects.filter(apartment_id=apartment.id)
        
        # get combinations of season/month
        season_month_dict = consumption_apartment_all.values("month", "season").distinct().order_by("-month").all()
        
        # set first month of season if season provided
        if season:
            
            # get first month for season
            month = season_month_dict.filter(season=season)[0]["month"]
        
        # if month is not in request or season is not provided, get the latest month
        if not month:
            month = season_month_dict[0]["month"]
        
        # try to get result or fail
        try:
            consumption_apartment = consumption_apartment_all.filter(month=month).first()
            consumption_building = ConsumptionReport.objects.filter(building_id = apartment.building.id, month=month, type="Building").first()
        except ConsumptionReport.DoesNotExist:
            consumption_apartment = None
            consumption_building = None
    
        
        # TODO TEST 
        return render(request, self.template_name, context={"apartment":apartment, "consumption_apartment": consumption_apartment, "consumption_building": consumption_building,
                                                            "season_month_dict": season_month_dict, "month": month, "season": season})
        
    
    
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
    
    
class PasswordResetView(View):
    
    def get(self,request, *args, **kwargs):
        password_reset_form = PasswordResetForm()
        return render(request=request, template_name="password_reset.html", context={"password_reset_form":password_reset_form})

    
    def post(self,request, *args, **kwargs):
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "password_reset_email.txt"
                    c = {
                        "username": user.username,
                        "email":user.email,
                        # 'domain':'127.0.0.1:8000',
                        'domain': settings.HOST,
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': default_token_generator.make_token(user),
                        'protocol': settings.PROTOCOL
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, None , [user.email], fail_silently=False)
                    except BadHeaderError:

                        return HttpResponse('Invalid header found.')
                        
                    messages.success(request, 'A message with reset password instructions has been sent to your inbox.')
            return redirect ("password_reset_done")