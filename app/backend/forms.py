import datetime

from django import forms
from django.forms import TextInput, PasswordInput, FileInput, Select

class LoginForm(forms.Form):
    username = forms.CharField(
        label="", 
        max_length=50, 
        required=True,
        widget=TextInput(attrs={
                'class': "form-control my-2",
                'placeholder': "Uporabniško ime"
            })
    )
    password = forms.CharField(
        label="", 
        required=True,
        widget=PasswordInput(attrs={
        'class': "form-control my-2",
        'placeholder': "Geslo"
        })
    ) 
    
class UploadUsersFromFileForm(forms.Form):
    file = forms.FileField(label="", required=True, widget=FileInput(attrs={
                'class': "form-control my-2",
            }))
    
    
    
class UploadConsumptionReportForm(forms.Form):
    
    today = datetime.date.today()
    this_year = today.year
    
    SEASON_CHOICES = list()
    MONTH_CHOICES = list()
    
    for i in range(0,3):
        choice = (f"{this_year-i}/{this_year-i+1}", f"{this_year-i}/{this_year-i+1}")
        SEASON_CHOICES.append(choice)
    
    
        for x in range(1,9):
            choice = (f"{this_year-i+1}_{x:02}", f"{this_year-i+1}_{x:02}")
            MONTH_CHOICES.append(choice)
            
        for y in range(9,13):
            choice = (f"{this_year-i}_{y:02}", f"{this_year-i}_{y:02}")
            MONTH_CHOICES.append(choice)
        
    
    
    season = forms.ChoiceField(label="Sezona", choices=SEASON_CHOICES, required=True,widget=Select(attrs={
                'class': "form-select my-2",
            }))
    month = forms.ChoiceField(label="Mesec", choices=MONTH_CHOICES, required=True, widget=Select(attrs={
                'class': "form-select my-2"
            }))
    file = forms.FileField(label="Datoteka", required=True, widget=FileInput(attrs={
                'class': "form-control my-2",
            }))