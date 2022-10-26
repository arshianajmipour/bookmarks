from django import forms
from django.contrib.auth.models import User
from .models import Profile, Report


class DateInput(forms.DateInput):
    input_type = 'date'


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password',
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo')


class ReportForm(forms.ModelForm):
    RADIO_BUTTON_CHOICES = (
        (1, 'select 1'),
        (2, 'select 2'),
        (3, 'select 3'),
    )
    radio_button_feature = forms.ChoiceField(choices=RADIO_BUTTON_CHOICES, widget=forms.RadioSelect, required=False, initial= 1)
    receive_newsletter = forms.BooleanField(label='Receive NewsLetter', required=False)

    class Meta:
        model = Report
        exclude = ('fpdf',)
        widgets = {
            'effective_date': DateInput(),
            'report_date': DateInput(),
        }
