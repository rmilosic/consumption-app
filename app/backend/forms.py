import datetime

from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label="Uporabniško ime", max_length=50, required=True)
    password = forms.CharField(label="Geslo", widget=forms.PasswordInput(), required=True) 
    
class UploadUsersFromFileForm(forms.Form):
    file = forms.FileField(label="Datoteka", required=True)
    
    
    
class UploadConsumptionReportForm(forms.Form):
    
    today = datetime.date.today()
    this_year = today.year
    
    SEASON_CHOICES = list()
    MONTH_CHOICES = list()
    
    for i in range(0,4):
        choice = (f"{this_year+i}/{this_year+i+1}", f"{this_year+i}/{this_year+i+1}")
        SEASON_CHOICES.append(choice)
    
    for i in range(0,4):
        for x in range(1,13):
            choice = (f"{this_year+i}_{x}", f"{this_year+i}_{x}")
            MONTH_CHOICES.append(choice)
        
    
    # TODO: prefill seasonss, months
    season = forms.ChoiceField(label="Sezona", choices=SEASON_CHOICES, required=True)
    month = forms.ChoiceField(label="Mesec", choices=MONTH_CHOICES, required=True)
    file = forms.FileField(label="Datoteka", required=True)