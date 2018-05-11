from django import forms
from django.contrib.auth import (
    authenticate,

    login,
    logout,
)
from django.contrib.auth.models import User




class UserLoginForm(forms.Form):
    
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username and password: 
            #firstly authenticate the user but does not log the user In
            user = authenticate(username = username, password = password)

            if not user.check_password(password):
                raise forms.ValidationError("Incorrect Password")


            if not user:
                raise forms.ValidationError("This User does not exist")

            if not user.is_active:
                raise forms.ValidationError("This User no longer exist")
            
            
        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegistrationForm(forms.ModelForm):
    email = forms.EmailField(
        required=True, label="Email Address"
    )
    email2 = forms.EmailField(
        label="Confirm Email"
    )
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model  =  User
        fields = (
            'username',
            'email',
            'email2',
            'password',
        )
    def clean_email2(self):
        email = self.cleaned_data.get("email")
        email2= self.cleaned_data.get("email2")

        if email != email2:
            raise forms.ValidationError("Email must match")

        # check if the email already exist
        email_qs = User.objects.filter(email = email)
        if email_qs.exists():
            raise forms.ValidationError("This Email has already been used by another user")
        return email