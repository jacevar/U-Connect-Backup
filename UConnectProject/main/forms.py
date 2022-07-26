
import datetime
from email.policy import default

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView

class DateInput(forms.DateInput):
    input_type = 'date'
class TimeInput(forms.DateInput):
    input_type = 'time'

class routesForms(forms.Form):
    cur_year = datetime.datetime.today().year
    year_range = tuple([i for i in range(cur_year - 2, cur_year + 10)])

    description = forms.CharField(max_length=300,min_length=1)
    startdate = forms.DateField(input_formats=['%Y-%m-%d'],widget=DateInput)
    startTime = forms.TimeField(input_formats=['%H:%M'],widget=TimeInput)
    #startdate = forms.DateField(input_formats=['%Y-%m-%d'], 
    #    widget=forms.SelectDateWidget(years=year_range))
    petfriendly = forms.BooleanField(required=False)
    route = forms.JSONField(widget = forms.HiddenInput())

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    class Meta:
        model = User
        fields = ['first_name','last_name','username', 'email', 'password1', 'password2',] 