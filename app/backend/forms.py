from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput()) 
    
class UploadUsersFromFileForm(forms.Form):
    file = forms.FileField()
    
    
    
class UploadConsumptionReportForm(forms.Form):
    
    # TODO: prefill seasonss, months
    season = forms.CharField(max_length=8)
    month = forms.CharField(max_length=8)
    file = forms.FileField()