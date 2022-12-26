import io
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
from django.http import HttpResponse, FileResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

from django.conf import settings

from reportlab.pdfgen import canvas

from .forms import LoginForm, UploadUsersFromFileForm, UploadConsumptionReportForm, ExportPdfForm
from .decorators import *
from .models import Building, Apartment, ConsumptionReport, Measurment

from backend.handlers import handle_file_upload_import_users, handle_file_upload_import_consumption
from backend.handlers import context

from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse

from weasyprint import HTML, CSS

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
            except Exception as e:
                # show success message
                messages.error(request, str(e))
                return render(request, self.template_name, {"form": form})
            
                
        else:
            form = UploadUsersFromFileForm()
            # show error message
        return render(request, self.template_name, {"form": form})
        
    def test_func(self):
        return is_admin(self.request.user)

    
class ConsumptionBulkImportView(UserPassesTestMixin, View):
    # form_class = MyForm
    # initial = {'key': 'value'}
    template_name = 'base_consumptionBulkImport.html'

    def get(self, request, *args, **kwargs):
        form = UploadConsumptionReportForm()
        # return render(request, self.template_name, {'form': form})
        return render(request, self.template_name, {'form': form})

    def test_func(self):
        return is_admin(self.request.user)
    
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
        
        user_context = context.get_user_context(month=month, season=season, owner_id=request.user.id)
        
        # get apartment
        # apartment = Apartment.objects.get(owner_id=request.user.id)
        
        # # get all apt reports  
        # consumption_apartment_all = ConsumptionReport.objects.filter(apartment_id=apartment.id)
        
        # # get combinations of season/month
        # season_month_dict = consumption_apartment_all.values("month", "season").distinct().order_by("-month").all()
        
        # # set first month of season if season provided
        # if season:
            
        #     # get first month for season
        #     month = season_month_dict.filter(season=season)[0]["month"]
        
        # # if month is not in request or season is not provided, get the latest month
        # if not month:
        #     month = season_month_dict[0]["month"]
        #     season = season_month_dict[0]["season"]
        
        # # try to get result or fail
        # try:
        #     consumption_apartment = consumption_apartment_all.filter(month=month).first()
        #     consumption_building = ConsumptionReport.objects.filter(building_id = apartment.building.id, month=month, type="Building").first()
        #     measurments = Measurment.objects.filter(consumption_report_id=consumption_apartment.id)
        # except ConsumptionReport.DoesNotExist:
        #     consumption_apartment = None
        #     consumption_building = None
        #     measurments = None
            
        form = ExportPdfForm(initial={"month": month, "season": season})
    
        
        return render(request, self.template_name, context={"apartment":user_context["apartment"], "consumption_apartment": user_context["consumption_apartment"], "consumption_building": user_context["consumption_building"],
                                                            "season_month_dict": user_context["season_month_dict"], "month": month, "season": season, "measurments":user_context["measurments"], "form": form})
        
    

    
    
class AdministratorView(View):
    # form_class = MyForm
    # initial = {'key': 'value'}
    template_name = 'base_admin.html'

    def get(self, request, *args, **kwargs):
        # form = self.form_class(initial=self.initial)
        # return render(request, self.template_name, {'form': form})
        return redirect("backend:consumptionBulkImport")
    
    
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
        
        
class ExportPdf(View):
    
    def post(self, request, *args, **kwargs):
        
        # buffer = io.BytesIO()

        # Create the PDF object, using the buffer as its "file."
        # p = canvas.Canvas(buffer)
        
        month = request.POST.get("month", None)
        season = request.POST.get("season", None)
        
        user_context = context.get_user_context(month, season, request.user.id)
        # html = render(request, )
        # print("month", month)
        
        # build user context
        template = get_template("base_user.html")
        # ctx = Context(user_context)
        user_context["user"]=request.user
        html = HTML(string=template.render(user_context))
        buffer = io.BytesIO()
        
        css = CSS(string='''
            @page { 
                size: A2 landscape; 
                margin: 0in 0.44in 0.2in 0.44in;
            }''')
        html.write_pdf(buffer, stylesheets=[css])
        

        # pdf = pisa.pisaDocument(io.BytesIO(html.encode()), result, encoding="utf-8")
        # get HTML of rendered template


        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        # p.drawString(100, 100, str(user_context["consumption_apartment"]))

        # Close the PDF object cleanly, and we're done.
        # p.showPage()
        # p.save()
        
        # if not pdf.err:
        #     return HttpResponse(result.getvalue(), content_type='application/pdf')
        # return HttpResponse('We had some errors<pre>%s</pre>')

        # FileResponse sets the Content-Disposition header so that browsers
        # present the option to save the file.
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='hello.pdf')
    
    
# def fetch_resources():
    