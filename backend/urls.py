"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from django.views.generic.base import RedirectView
from django.contrib.auth.decorators import login_required, permission_required


from .views import *

app_name = 'backend'


urlpatterns = [
    path("", login_required(IndexView.as_view()), name="index"),
    path('prijava/', LoginView.as_view(), name="login"),
    # path('odjava/', LogoutView.as_view(), name="logout"),
    path('uporabnik/', login_required(UserView.as_view()), name="user"),
    path('uvoz-uporabnikov/', UsersBulkImportView.as_view(), name="usersBulkImport"),
    path('uvoz-porabe/', ConsumptionBulkImportView.as_view(), name="consumptionBulkImport"),
    path('poraba/', ConsumptionView.as_view(), name="consumption"),
    path('administrator/', AdministratorView.as_view(), name="administrator")
]
